// Copyright (c) 2020, Havenir Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on("Meter Reading", {
	refresh: function(frm) {
		if (frm.is_new()) {
			frm.trigger('filling_station');
		}
	},
	filling_station: function(frm) {
		if (frm.doc.filling_station) {
			frm.call('fetch_meters');
		}else{
			frm.set_value('meter_reading_detail', []);
		}
	}
});
frappe.ui.form.on("Meter Reading Detail", {
	new_qty: function(frm, cdt, cdn) {
		let row = frappe.get_doc(cdt, cdn);
		if (row.new_qty){
			if (row.new_qty < row.qty) {
				frappe.model.set_value(cdt, cdn, 'new_qty', row.qty);
				frm.refresh_field('meter_reading_detail');
				frappe.msgprint('New Meter Reading (New Qty) can not be less than Previous meter reading (Qty)')
			} else {
				const sales_revenue = (row.new_qty - row.qty) * row.rate;
				frappe.model.set_value(cdt, cdn, 'sales_revenue', sales_revenue.toFixed(3));
				frm.refresh_field('meter_reading_detail');
			}
		}else {
			frappe.model.set_value(cdt, cdn, 'new_qty', row.qty);
		}
		calculate_revenue(frm);
	},
	actual_total_revenue: function(frm, cdt, cdn) {
		let row = frappe.get_doc(cdt, cdn);
		if (!row.actual_total_revenue) {
			row.actual_total_revenue = 0;
		}
		calculate_revenue(frm);
	}
});
frappe.ui.form.on("Mode of Payment Detail", {
	amount: function(frm, cdt, cdn) {
		let row = frappe.model.get_doc(cdt, cdn);
		if (row.amount < 0) {
			frappe.model.set_value(cdt, cdn, 'amount', 0);
			frm.refresh_field('mode_of_payment')
			frappe.msgprint('Amount must be greater than zero', 'Invalid Amount')
		}
	}
});

const calculate_revenue = (frm) => {
	var sales_revenue = 0;
	var total_revenue = 0;
	for (const row of frm.doc.meter_reading_detail) {
		sales_revenue += parseFloat(row.sales_revenue);
		total_revenue += parseFloat(row.actual_total_revenue);
	}
	frm.set_value('sales_revenue', sales_revenue);
	frm.set_value('total_actual_revenue', total_revenue);
	frm.refresh_field(['sales_revenue', 'total_actual_revenue']);
}