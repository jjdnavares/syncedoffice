# Copyright (c) 2025, jumes.dev and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def create_content_type(data):
	"""Create a new content type"""
	doc = frappe.get_doc({
		"doctype": "CMS Content Type",
		**data
	})
	doc.insert()
	frappe.db.commit()
	return doc


def update_content_type(name, data):
	"""Update an existing content type"""
	doc = frappe.get_doc("CMS Content Type", name)
	doc.update(data)
	doc.save()
	frappe.db.commit()
	return doc


def delete_content_type(name):
	"""Delete a content type"""
	frappe.delete_doc("CMS Content Type", name)
	frappe.db.commit()
	return {"message": "Content type deleted successfully"}


def get_content_type(name):
	"""Get a single content type with all fields"""
	doc = frappe.get_doc("CMS Content Type", name)
	return doc.as_dict()


def list_content_types(filters=None):
	"""List all content types"""
	filters = filters or {}
	content_types = frappe.get_all(
		"CMS Content Type",
		filters=filters,
		fields=["name", "content_type_name", "display_name", "kind", "api_id", "is_published", "icon", "modified"]
	)
	return content_types


def validate_content_type_schema(data):
	"""Validate content type schema"""
	errors = []

	# Validate required fields
	if not data.get("content_type_name"):
		errors.append("Content type name is required")
	
	if not data.get("display_name"):
		errors.append("Display name is required")
	
	if not data.get("kind"):
		errors.append("Kind is required")

	# Validate fields
	if data.get("fields"):
		field_names = []
		for idx, field in enumerate(data["fields"]):
			if not field.get("field_name"):
				errors.append(f"Field name is required for field at position {idx + 1}")
			elif field["field_name"] in field_names:
				errors.append(f"Duplicate field name: {field['field_name']}")
			else:
				field_names.append(field["field_name"])

			if not field.get("field_type"):
				errors.append(f"Field type is required for field '{field.get('field_name', idx + 1)}'")

	if errors:
		frappe.throw("<br>".join(errors))

	return True


def get_content_type_by_api_id(api_id):
	"""Get content type by API ID"""
	# Check cache first
	cache_key = f"cms_content_type:{api_id}"
	cached = frappe.cache().get_value(cache_key)
	
	if cached:
		return cached

	# Query database
	name = frappe.db.get_value("CMS Content Type", {"api_id": api_id}, "name")
	if not name:
		frappe.throw(_("Content type not found: {0}").format(api_id), frappe.DoesNotExistError)

	doc = frappe.get_doc("CMS Content Type", name)
	result = doc.as_dict()

	# Cache for 5 minutes
	frappe.cache().set_value(cache_key, result, expires_in_sec=300)
	
	return result
