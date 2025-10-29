# Copyright (c) 2025, jumes.dev and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def add_field(content_type, field_data):
	"""Add a field to a content type"""
	doc = frappe.get_doc("CMS Content Type", content_type)
	
	# Set position if not provided
	if not field_data.get("position"):
		field_data["position"] = len(doc.fields) + 1
	
	doc.append("fields", field_data)
	doc.save()
	frappe.db.commit()
	
	return doc


def update_field(content_type, field_name, data):
	"""Update a field in a content type"""
	doc = frappe.get_doc("CMS Content Type", content_type)
	
	# Find the field
	field_found = False
	for field in doc.fields:
		if field.field_name == field_name:
			field.update(data)
			field_found = True
			break
	
	if not field_found:
		frappe.throw(_("Field not found: {0}").format(field_name))
	
	doc.save()
	frappe.db.commit()
	
	return doc


def delete_field(content_type, field_name):
	"""Delete a field from a content type"""
	doc = frappe.get_doc("CMS Content Type", content_type)
	
	# Find and remove the field
	field_found = False
	for idx, field in enumerate(doc.fields):
		if field.field_name == field_name:
			doc.fields.pop(idx)
			field_found = True
			break
	
	if not field_found:
		frappe.throw(_("Field not found: {0}").format(field_name))
	
	doc.save()
	frappe.db.commit()
	
	return {"message": "Field deleted successfully"}


def reorder_fields(content_type, field_order):
	"""Reorder fields in a content type
	
	Args:
		content_type: Name of the content type
		field_order: List of field names in desired order
	"""
	doc = frappe.get_doc("CMS Content Type", content_type)
	
	# Create a mapping of field_name to field object
	field_map = {field.field_name: field for field in doc.fields}
	
	# Reorder fields
	new_fields = []
	for idx, field_name in enumerate(field_order):
		if field_name in field_map:
			field = field_map[field_name]
			field.position = idx + 1
			new_fields.append(field)
	
	# Replace fields with reordered list
	doc.fields = new_fields
	doc.save()
	frappe.db.commit()
	
	return doc


def validate_field_config(field_data):
	"""Validate field configuration"""
	errors = []
	
	# Required fields
	if not field_data.get("field_name"):
		errors.append("Field name is required")
	
	if not field_data.get("field_label"):
		errors.append("Field label is required")
	
	if not field_data.get("field_type"):
		errors.append("Field type is required")
	
	# Validate field name format
	if field_data.get("field_name"):
		field_name = field_data["field_name"]
		if not field_name.replace("_", "").isalnum():
			errors.append("Field name must contain only letters, numbers, and underscores")
	
	# Validate field type specific options
	field_type = field_data.get("field_type")
	options = field_data.get("options")
	
	if field_type == "Relation" and options:
		if not options.get("target"):
			errors.append("Relation field must specify a target content type")
	
	elif field_type == "Component" and options:
		if not options.get("component"):
			errors.append("Component field must specify a component reference")
	
	elif field_type == "Enumeration" and options:
		if not options.get("values"):
			errors.append("Enumeration field must specify values")
	
	if errors:
		frappe.throw("<br>".join(errors))
	
	return True
