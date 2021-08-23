frappe.listview_settings['Sales Entry'] = {
    fields : ['status'],

    get_indicator: function (doc) {
        if (doc.status === "Completed") {
            return [__("Completed"), "green", "status,=,Completed"];
        } else if (doc.status === "To Bill") {
            return [__("To Bill"), "orange", "status,=,To Bill"];
        } else if (doc.status === "Draft") {
            return [__("Draft"), "red", "status,=,Draft"];
        }
    }
};