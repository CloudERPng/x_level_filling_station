import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_field
from erpnext.accounts.doctype.accounting_dimension.accounting_dimension import get_accounting_dimensions


def make_dimension_in_accounting_doctypes(doc, method):
	'''
	On after insert event: Creates Custom Field in Filling Staion
	in the Accounting Dimensions Section
	'''
	doc_count = len(get_accounting_dimensions())
	
	if (doc_count) % 2 == 0:
		insert_after_field = 'dimension_col_break'
	else:
		insert_after_field = 'accounting_dimensions_section'

	df = {
		"fieldname": doc.fieldname,
		"label": doc.label,
		"fieldtype": "Link",
		"options": doc.document_type,
		"insert_after": insert_after_field,
		"owner": "Administrator"
	}

	meta = frappe.get_meta('Filling Station', cached=False)
	fieldnames = [d.fieldname for d in meta.get("fields")]

	if df['fieldname'] not in fieldnames:
		create_custom_field('Filling Station', df)

	frappe.clear_cache(doctype='Filling Station')


def delete_accounting_dimension(doc, method):
	'''
	On Trash: deletes the Accounting Dimension from Filling Station
	'''
	doclist = ['Filling Station']

	frappe.db.sql("""
		DELETE FROM `tabCustom Field`
		WHERE fieldname = %s
		AND dt IN (%s)""" %			#nosec
		('%s', ', '.join(['%s']* len(doclist))), tuple([doc.fieldname] + doclist))

	frappe.db.sql("""
		DELETE FROM `tabProperty Setter`
		WHERE field_name = %s
		AND doc_type IN (%s)""" %		#nosec
		('%s', ', '.join(['%s']* len(doclist))), tuple([doc.fieldname] + doclist))

def disable_dimension(doc, method):
	'''
	On Validate: makes the field readonly is disabled nad viceversa
	'''
	if doc.get('disabled'):
		df = {"read_only": 1}
	else:
		df = {"read_only": 0}
		
	field = frappe.db.get_value("Custom Field", {"dt": 'Filling Station', "fieldname": doc.get('fieldname')})
	if field:
		custom_field = frappe.get_doc("Custom Field", field)
		custom_field.update(df)
		custom_field.save()

	frappe.clear_cache(doctype='Filling Station')