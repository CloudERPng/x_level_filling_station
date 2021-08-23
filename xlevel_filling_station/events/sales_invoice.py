import frappe

def on_submit(doc, method):
    '''
    Updates Filling Stations - Sales Entry Document
    1- Status
    2- Sales Invoice
    '''
    sales_entry = ''
    for row in doc.items:
        sales_entry = row.sales_entry
        break
    frappe.db.set_value('Sales Entry', sales_entry, 'sales_invoice', doc.name)
    frappe.db.set_value('Sales Entry', sales_entry, 'status', 'Completed')

def on_cancel(doc, method):
    '''
    Updates Filling Stations - Sales Entry Document
    1- Status
    2- Sales Invoice
    '''
    sales_entry = ''
    for row in doc.items:
        sales_entry = row.sales_entry
        frappe.db.set_value('Sales Entry', sales_entry, 'status', 'To Bill')
        frappe.db.set_value('Sales Entry', sales_entry, 'sales_invoice', None)