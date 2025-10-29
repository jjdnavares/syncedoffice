import frappe

no_cache = 1


def get_context(context):
	"""Context for CMS SPA"""
	context.no_cache = 1
	
	# Check if user has permission
	if frappe.session.user == "Guest":
		frappe.throw("Please login to access CMS", frappe.PermissionError)
	
	return context
