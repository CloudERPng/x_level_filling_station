# -*- coding: utf-8 -*-
# Copyright (c) 2020, Havenir Solutions and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class MeterReading(Document):
	def on_submit(self):
		self.db_set('status', 'To Sales Entry')
		self.current_reading()

	def on_cancel(self):
		self.db_set('status', 'Canceled')
		self.current_reading_on_cancel()

	def validate(self):
		self.validate_revenue()

	@frappe.whitelist()
	def fetch_meters(self):
		price_list = frappe.db.get_value(
			'Filling Station', self.filling_station, 'price_list')
		meters = frappe.db.get_list('Meter', {
			'filling_station': self.filling_station
		}, ['name', 'qty', 'item_code'])
		self.meter_reading_detail = []
		for row in meters:
			rate = frappe.db.get_value('Item Price', {
			'item_code': row.item_code,
			'price_list': price_list
			}, 'price_list_rate')
			self.append('meter_reading_detail', {
				'meter': row.name,
				'item_code': row.item_code,
				'qty': row.qty,
				'new_qty': row.qty,
				'rate': rate
			})
	
	def current_reading(self):
		for row in self.meter_reading_detail:
			frappe.db.set_value('Meter', row.meter, 'qty', row.new_qty)

	def current_reading_on_cancel(self):
		for row in self.meter_reading_detail:
			meter = frappe.get_doc('Meter', row.meter)
			if row.new_qty - row.qty != 0:
				meter.db_set('qty', meter.qty - (row.new_qty - row.qty))

	def validate_revenue(self):
		amount = 0
		for row in self.mode_of_payment:
			amount += row.amount
		if amount != self.total_actual_revenue:
			frappe.throw('Sum of Amount in <b>Mode of Payment</b> should be equal to <b>Total Actual Revenue</b>', title = '<b>Invalid Result</b>')
	
