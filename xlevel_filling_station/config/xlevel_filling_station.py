from __future__ import unicode_literals
from frappe import _


def get_data():
    return [
        {
        "label":
        _("Filling Station"),
        "items": [
            {
                "type": "doctype",
                "name": "Meter Reading",
                "options": "Meter Reading"
            },
            {
                "type": "doctype",
                "name": "Sales Entry",
                "options": "Sales Entry"
            }
        ]},
        {
        "label":
        _("Setup"),
        "items": [
            {
                "type": "doctype",
                "name": "Filling Station",
                "options": "Filling Station"
            },
            {
                "type": "doctype",
                "name": "Fuel Tank",
                "options": "Fuel Tank"
            },
            {
                "type": "doctype",
                "name": "Meter",
                "options": "Meter"
            }
        ]}
    ]
