import frappe


def has_app_permission():
	"""Check if user has permission to access SyncedOffice app."""
	# Allow all logged-in users to access the app
	# You can customize this logic based on your requirements
	return True
