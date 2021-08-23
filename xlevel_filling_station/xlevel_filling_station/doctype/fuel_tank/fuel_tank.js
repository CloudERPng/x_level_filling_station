// Copyright (c) 2020, Havenir Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on('Fuel Tank', {
	filling_station: function (frm) {
		frm.set_value('warehouse', null);
		if (frm.doc.filling_station){
			frm.set_query('warehouse', () => {
				return {
					filters : {
						is_group: 0,
						warehouse_type: 'Fuel Tank',
						parent_warehouse: frm.doc.filling_station
					}
				}
			})
		}
	}
});
