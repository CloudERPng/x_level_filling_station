# -*- coding: utf-8 -*-
# Copyright (c) 2020, Havenir Solutions and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

from erpnext.stock.doctype import stock_reconciliation
import frappe
from frappe import _
import datetime
from frappe.model.document import Document

class SalesEntry(Document):
	def on_submit(self):
		self.validate_meter_readings()
		self.update_meter_readings()
		self.create_sales_invoice()
		self.create_stock_reconciliation()
		self.db_set('status', 'Completed')
	
	def on_cancel(self):
		self.db_set('status', 'Canceled')
		self.update_meter_readings_oncancel()

	def validate(self):
		self.update_values()

	def validate_meter_readings(self):
		for row in self.meter_readings:
			status = frappe.db.get_value('Meter Reading',row.meter_reading ,'status')
			if status == 'Completed':
				frappe.throw(f'Row# {row.idx}:  Status of Meter Reading# {row.meter_reading} is set to Completed')
				
	@frappe.whitelist()
	def fetch_meters(self):
		qty_via_meter = {}
		self.meter_readings = []
		self.fuel_tank = []
		self.mode_of_payment = []
		total_sales_revenue = 0
		total_actual_revenue = 0
		payments = {}
		item_rate = {}
		#Fetch all meter readings against selected filling station in current date
		meter_readings = frappe.get_all('Meter Reading', {
			'filling_station': self.filling_station,
			'posting_date': self.posting_date,
			'company': self.company,
			'status': 'To Sales Entry'
		}, ['name', 'sales_revenue', 'total_actual_revenue'])

		for meter in meter_readings:
			# Sum total revenues
			total_sales_revenue += meter.sales_revenue
			total_actual_revenue += meter.total_actual_revenue

			#populate meter reading table
			meter_reading = frappe.get_all('Meter Reading Detail', {
				'parent': meter.name,
			}, ['name' ,'meter', 'qty', 'new_qty', 'rate', 'sales_revenue', 'actual_total_revenue'])

			for row in meter_reading:
				item_code, item_name = frappe.db.get_value('Meter', row.meter, ['item_code', 'item_name'])
				item_rate[item_code] = row.rate
				if row.sales_revenue != 0:
					self.append('meter_readings', {
						'meter': row.meter,
						'item_code': item_code,
						'item_name': item_name,
						'qty': row.qty,
						'new_qty': row.new_qty,
						'rate': row.rate,
						'amount': row.sales_revenue,
						'actual_amount': row.actual_total_revenue,
						'meter_reading': meter.name,
						'meter_reading_detail': row.name
					})

				#Accumulating quantity of each item against all meters
				meter_qty = row.new_qty-row.qty
				if item_code not in qty_via_meter.keys():
					qty_via_meter[item_code] = meter_qty
				else:
					qty_via_meter[item_code] += meter_qty

			#populate mode of payment detail table
			mode_of_payment = frappe.get_all('Mode of Payment Detail', {
				'parent': meter.name,
			},['mode_of_payment', 'amount'])
			
			for row in mode_of_payment:
				if row.mode_of_payment not in payments:
					payments[row.mode_of_payment] = row.amount
				else:
					payments[row.mode_of_payment] += row.amount
		
		# Populating Payments Section
		for key, value in payments.items():
			self.append('mode_of_payment', {
				'mode_of_payment': key,
				'amount': value
			})
		#populate fuel tank detail table
		self.fuel_tank_detail = []
		for item in qty_via_meter:
			#Fetching values
			filters = {'item_code': item, 'filling_station': self.filling_station}
			fuel_tank, item_code, item_name = frappe.db.get_value(
				'Fuel Tank', filters, ['name', 'item_code', 'item_name'])

			filters = {'item_code': item, 'warehouse': fuel_tank}
			qty = frappe.db.get_value('Bin', filters, 'actual_qty')
			# item_code = frappe.db.get_value('Fuel Tank', filters, 'item_code')

			if not qty:
				frappe.throw(_(f'No Stock Available for {item}'))

			exp_qty = qty - qty_via_meter[item]

			self.append('fuel_tank_detail', {
				'fuel_tank': fuel_tank,
				'item_code': item_code,
				'item_name': item_name,
				'rate': item_rate[item_code],
				'amount': item_rate[item_code] * qty_via_meter[item],
				'opening_qty': qty,
				'qty_via_meter': qty_via_meter[item],
				'expected_closing_qty': exp_qty,
				'actual_qty': exp_qty
			})
		
		self.total_sales_revenue = total_sales_revenue
		self.total_actual_revenue = total_actual_revenue
	
	def update_values(self):
		for row in self.fuel_tank_detail:
			row.expected_closing_qty = row.opening_qty - row.qty_via_meter
			row.difference = row.actual_qty - row.expected_closing_qty
	
	def create_sales_invoice(self):
		customer = frappe.db.get_value('Company', self.company, 'filling_station_customer')
		filling_station_doc = frappe.get_doc('Filling Station', self.filling_station)
		meta = frappe.get_meta("Filling Station")
		doc = frappe.new_doc('Sales Invoice')
		doc.set_posting_time = 1
		doc.posting_date = self.posting_date
		doc.is_pos = 1
		doc.update_stock = 1
		doc.company = self.company
		doc.write_off_outstanding_amount_automatically = 1
		doc.write_off_account = frappe.db.get_value('Company', self.company, 'write_off_account')
		doc.write_off_cost_center = filling_station_doc.cost_center
		doc.write_off_amount = self.total_sales_revenue - self.total_actual_revenue
		if not customer:
			frappe.throw('Default customer is not set')
		doc.customer = customer
		doc.due_date = datetime.datetime.now().date()
		
		# Setting Dimensions
		for field in meta.get('fields'):
			if field.fieldname not in ['name', 'warehouse'] and hasattr(doc, field.fieldname):
				setattr(doc, field.fieldname, getattr(filling_station_doc, field.fieldname))

		# Updating Items
		for row in self.fuel_tank_detail:
			item_row = doc.append('items', {
				'item_code': row.item_code,
				'item_name': row.item_name,
				'qty': row.qty_via_meter,
				'warehouse': row.fuel_tank,
				'rate': row.rate,
				'amount': row.amount,
				'sales_entry': self.name,
				'fuel_tank_detail': row.name
			})

			# Updating Dimensions for each item
			for field in meta.get('fields'):
				if field.fieldname not in ['name', 'warehouse'] and hasattr(item_row, field.fieldname):
					setattr(item_row, field.fieldname, getattr(filling_station_doc, field.fieldname))

		# Updating Payments
		for payment in self.mode_of_payment:
			doc.append('payments', {
				'mode_of_payment': payment.mode_of_payment,
				'amount': payment.amount
			})

		doc.save()
		doc.submit()
		frappe.msgprint(f'Sales Invoice {doc.name} Submitted')
		self.db_set('sales_invoice', doc.name)
		return doc.name
	
	def create_stock_reconciliation(self):
		stock_diff = {}
		for row in self.fuel_tank_detail:
			if row.difference != 0:
				stock_diff[(row.item_code, row.fuel_tank)] = row.actual_qty

		if not bool(stock_diff):
			return

		stock_reconciliation_doc = frappe.get_doc({
			'doctype': 'Stock Reconciliation',
			'sales_entry': self.name,
			'posting_date': self.posting_date,
			'purpose': 'Stock Reconciliation',
			'set_posting_time': 1,
			'expense_account': frappe.db.get_value('Company', self.company, 'stock_adjustment_account')
		})

		# Setting Dimensions
		filling_station_doc = frappe.get_doc('Filling Station', self.filling_station)
		meta = frappe.get_meta("Filling Station")
		for field in meta.get('fields'):
			if field.fieldname not in ['name', 'warehouse'] \
				and hasattr(stock_reconciliation_doc, field.fieldname):
				setattr(
					stock_reconciliation_doc, 
					field.fieldname, 
					getattr(filling_station_doc, field.fieldname)
				)		

		# Setting Items
		for row in stock_diff:
			stock_reconciliation_doc.append('items', {
				'item_code': row[0],
				'warehouse': row[1],
				'qty': stock_diff[row],
				'valuation_rate': frappe.db.get_value('Bin', {
					'item_code': row[0],
					'warehouse': row[1]
				}, 'valuation_rate')
			})

		stock_reconciliation_doc.save()
		stock_reconciliation_doc.submit()
		frappe.msgprint(_(f'Stock Reconciliation {stock_reconciliation_doc.name} Submitted'))
		self.db_set('stock_reconciliation', stock_reconciliation_doc.name)
		return stock_reconciliation_doc.name

	def update_meter_readings(self):
		for row in self.meter_readings:
			frappe.db.set_value('Meter Reading', row.meter_reading, 'status', 'Completed')
		
	def update_meter_readings_oncancel(self):
		for row in self.meter_readings:
			frappe.db.set_value('Meter Reading', row.meter_reading, 'status', 'To Sales Entry')
