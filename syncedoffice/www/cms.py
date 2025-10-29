import frappe
from syncedoffice.so_cms.utils import get_cms_assets

no_cache = 1


def get_context(context):
	"""Context for CMS SPA"""
	context.no_cache = 1
	
	# Check if user has permission
	if frappe.session.user == "Guest":
		frappe.throw("Please login to access CMS", frappe.PermissionError)
	
	# Add cache control headers
	frappe.response["Cache-Control"] = "no-cache, no-store, must-revalidate"
	frappe.response["Pragma"] = "no-cache"
	frappe.response["Expires"] = "0"
	
	# Get CMS assets from Vite manifest
	assets = get_cms_assets()
	context.cms_css = assets['css']
	context.cms_js = assets['js']
	
	return context
