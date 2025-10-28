# Stub file for customer module
# This is a placeholder until the full selling module is implemented

import frappe
from frappe.model.document import Document

def parse_full_name(full_name):
	"""Parse full name into first, middle, and last name"""
	parts = full_name.strip().split()
	
	if len(parts) == 0:
		return {"first_name": "", "middle_name": "", "last_name": ""}
	elif len(parts) == 1:
		return {"first_name": parts[0], "middle_name": "", "last_name": ""}
	elif len(parts) == 2:
		return {"first_name": parts[0], "middle_name": "", "last_name": parts[1]}
	else:
		return {
			"first_name": parts[0],
			"middle_name": " ".join(parts[1:-1]),
			"last_name": parts[-1]
		}

class Customer(Document):
	"""Stub Customer DocType"""
	pass
