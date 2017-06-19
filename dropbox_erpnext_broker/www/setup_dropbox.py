import frappe
import requests
from frappe import _
from frappe.integrations.doctype.dropbox_settings.dropbox_settings import (get_dropbox_authorize_url,
	dropbox_auth_finish)

no_cache = 1

@frappe.whitelist(allow_guest=True)
def get_authotize_url(site):
	dropbox_auth_args = get_dropbox_authorize_url()
	set_site_dropbox_token(site, dropbox_auth_args["args"]["state"][0])
	return dropbox_auth_args

def set_site_dropbox_token(site, state):
	frappe.get_doc({
		"doctype": "Site Dropbox Token",
		"site_name": site,
		"token_state": state
	}).insert(ignore_permissions=True)

	frappe.db.commit()

@frappe.whitelist(allow_guest=True)
def generate_dropbox_access_token():
	access_token, state = dropbox_auth_finish(return_access_token=True)
	update_access_token_to_site(access_token, state)

def update_access_token_to_site(access_token, state):
	close = '<p class="text-muted">' + _('Please close this window') + '</p>'
	token_details = frappe.get_doc("Site Dropbox Token", state)
	
	url = "{0}/api/method/frappe.integrations.doctype.dropbox_settings.dropbox_settings.set_dropbox_access_token".format(token_details.site_name)
	res = requests.post(url, data={"access_token": access_token})
	
	frappe.respond_as_web_page(_("Dropbox Setup"),
		_("Dropbox access is approved!") + close,
		indicator_color='green')