# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "xlevel_filling_station"
app_title = "Xlevel Filling Station"
app_publisher = "Havenir Solutions"
app_description = "Xlevel Filling Station"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "info@havenir.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/xlevel_filling_station/css/xlevel_filling_station.css"
# app_include_js = "/assets/xlevel_filling_station/js/xlevel_filling_station.js"

# include js, css files in header of web template
# web_include_css = "/assets/xlevel_filling_station/css/xlevel_filling_station.css"
# web_include_js = "/assets/xlevel_filling_station/js/xlevel_filling_station.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "xlevel_filling_station.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "xlevel_filling_station.install.before_install"
# after_install = "xlevel_filling_station.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "xlevel_filling_station.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Sales Invoice": {
        'on_submit': 'xlevel_filling_station.events.sales_invoice.on_submit',
        'on_cancel': 'xlevel_filling_station.events.sales_invoice.on_cancel'
    },
    "Accounting Dimension" : {
        'after_insert': 'xlevel_filling_station.events.accounting_dimension.make_dimension_in_accounting_doctypes',
        'on_trash': 'xlevel_filling_station.events.accounting_dimension.delete_accounting_dimension',
        'validate': 'xlevel_filling_station.events.accounting_dimension.disable_dimension'
    }
}

#Fixtures
fixtures = [
	{"dt": "Custom Field",
    "filters": [["name", "in", [
        'Sales Invoice Item-sales_entry',
        'Sales Invoice Item-fuel_tank_detail',
        'Company-filling_station_customer',
        'Stock Reconciliation-sales_entry'
        ]]]}
]

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"xlevel_filling_station.tasks.all"
# 	],
# 	"daily": [
# 		"xlevel_filling_station.tasks.daily"
# 	],
# 	"hourly": [
# 		"xlevel_filling_station.tasks.hourly"
# 	],
# 	"weekly": [
# 		"xlevel_filling_station.tasks.weekly"
# 	]
# 	"monthly": [
# 		"xlevel_filling_station.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "xlevel_filling_station.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "xlevel_filling_station.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "xlevel_filling_station.task.get_dashboard_data"
# }

