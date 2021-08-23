frappe.listview_settings['Meter Reading'] = {
    fields : ['status'],

    get_indicator: function (doc) {
        if (doc.status === "Completed") {
            return [__("Completed"), "green", "status,=,Completed"];
        } else if (doc.status === "To Sales Entry") {
            return [__("To Sales Entry"), "orange", "status,=,To Sales Entry"];
        } else if (doc.status === "Draft") {
            return [__("Draft"), "red", "status,=,Draft"];
        }
    }
};