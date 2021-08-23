// Copyright (c) 2020, Havenir Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sales Entry', {
	refresh: function(frm) {
		if(frm.is_new()) {
			frm.trigger('filling_station');
		}
		if (frm.doc.docstatus === 0) {
			frm.add_custom_button('Fetch Meter Readings', () => {
				if (frm.doc.filling_station && frm.doc.posting_date) {
					frm.call('fetch_meters');
				} else {
					frappe.msgprint('Select Filling Station and Posting Date First');
				}
			});
		}
		if (frm.doc.status === 'To Bill') {
			frm.add_custom_button('Create Sales Invoice', () => {
				frm.call('create_sales_invoice')
				.then(r => {
					if(r.message) {
						frappe.show_alert(`Sales Invoice<a href="#Form/Sales%20Invoice/${r.message}">${r.message}</a> Created`)
					}
				})
			});
		}
	},
	filling_station: function(frm) {
		frm.doc.meter_readings = [];
		frm.doc.fuel_tank_detail = [];
		frm.doc.mode_of_payment = [];
		frm.doc.total_sales_revenue = null;
		frm.doc.total_actual_revenue = null;
		frm.refresh_fields('meter_reading', 'fuel_tank_detail', 'mode_of_payment')
		if (frm.doc.filling_station){
			frm.call('fetch_meters');
		}
	},
	posting_date: function(frm) {
		frm.doc.meter_reading = [];
		frm.doc.fuel_tank_detail = [];
		frm.doc.mode_of_payment = [];
		frm.refresh_fields('meter_reading', 'fuel_tank_detail', 'mode_of_payment');
		if (frm.doc.posting_date) {
			frm.call('fetch_meters');
		}
	}
});
frappe.ui.form.on('Fuel Tank Detail', {
	received_qty: function(frm, cdt, cdn) {
		let row = frappe.model.get_doc(cdt, cdn)
		let exp_qty;
		if (row.received_qty) {
			exp_qty = row.opening_qty + row.received_qty - row.qty_via_meter;
		} else {
			exp_qty = row.opening_qty - row.qty_via_meter;
		}
		frappe.model.set_value(cdt, cdn, 'expected_closing_qty', exp_qty);
		frm.refresh_field('dip_stick_detail');
	},
	actual_qty: function(frm, cdt, cdn) {
		let row = frappe.model.get_doc(cdt, cdn)
		if (!row.actual_qty < 0 || row.actual_qty < 0) {
			frappe.model.set_value(cdt, cdn, 'actual_qty', 0)
		}
		const difference = row.actual_qty - row.expected_closing_qty;
		frappe.model.set_value(cdt, cdn, 'difference', difference);
		
		frm.refresh_field('dip_stick_detail');
	},
	expected_closing_qty: function(frm, cdt, cdn) {
		let row = frappe.model.get_doc(cdt, cdn)
		if (row.actual_qty && row.expected_closing_qty) {
			const difference = row.actual_qty - row.expected_closing_qty;
			frappe.model.set_value(cdt, cdn, 'difference', difference);
			frm.refresh_field('dip_stick_detail');
		}
	}
});
