# -*- coding: utf-8 -*-
# Copyright (c) 2020, Havenir Solutions and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class FillingStation(Document):
	def fetch_meters(self):
		self.filling_station_detail = []
		meters = frappe.db.get_list('Meter', {
			'filling_station': self.warehouse
		}, ['name', 'qty', 'rate', 'item_code', 'item_name'])
		for row in meters:
			self.append('filling_station_detail', {
				'meter': row.name,
				'qty': row.qty,
				'rate': row.rate,
				'item_code': row.item_code,
				'item_name': row.item_name
			})
