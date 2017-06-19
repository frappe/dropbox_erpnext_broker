// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// MIT License. See license.txt

frappe.ready(function() {
	$('.btn-next').off("click").on("click", function() {
		frappe.call({
			method: "dropbox_erpnext_broker.www.setup_dropbox.get_authotize_url",
			args:{
				"site": "{{ frappe.form_dict.site }}"
			},
			freeze: true,
			callback: function(r) {
				if(!r.exc) {
					window.open(r.message.auth_url, "_self");
				}
			}
		})
	})
})
