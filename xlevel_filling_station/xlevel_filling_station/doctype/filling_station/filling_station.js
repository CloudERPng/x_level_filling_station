// Copyright (c) 2020, Havenir Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on('Filling Station', {
	refresh: function (frm) {
		frm.set_query('warehouse', () => {
			return {
				filters : {
					is_group: 1,
					warehouse_type: 'Filling Station'
				}
			}
		})
	}
});