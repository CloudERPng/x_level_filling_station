// Copyright (c) 2020, Havenir Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on('Meter', {
	qty: function(frm) {
		if (frm.doc.qty < 0) {
			frm.set_value('qty', 0);
			frappe.msgprint('Current Meter Reading Qty can not be less than zero');
		}
	},
	filling_station: function (frm) {
		if (frm.doc.filling_station){
			frm.set_query('fuel_tank', () => {
				return {
					filters : {
						filling_station: frm.doc.filling_station
					}
				}
			})
		}
	}
});
