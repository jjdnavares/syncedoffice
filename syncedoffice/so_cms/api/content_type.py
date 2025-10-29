# Copyright (c) 2025, jumes.dev and contributors
# For license information, please see license.txt

import frappe
from syncedoffice.so_cms.services import content_type_service, field_service


@frappe.whitelist()
def get_content_types(filters=None):
	"""Get all content types
	
	Returns:
		list: List of content types
	"""
	try:
		filters = frappe.parse_json(filters) if filters else {}
		return content_type_service.list_content_types(filters)
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "CMS API Error: get_content_types")
		frappe.throw(str(e))


@frappe.whitelist()
def get_content_type(name):
	"""Get a single content type with all fields
	
	Args:
		name: Name of the content type
		
	Returns:
		dict: Content type details
	"""
	try:
		return content_type_service.get_content_type(name)
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "CMS API Error: get_content_type")
		frappe.throw(str(e))


@frappe.whitelist()
def create_content_type(data):
	"""Create a new content type
	
	Args:
		data: Content type data (JSON string or dict)
		
	Returns:
		dict: Created content type
	"""
	try:
		data = frappe.parse_json(data) if isinstance(data, str) else data
		
		# Validate schema
		content_type_service.validate_content_type_schema(data)
		
		# Create content type
		doc = content_type_service.create_content_type(data)
		return doc.as_dict()
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "CMS API Error: create_content_type")
		frappe.throw(str(e))


@frappe.whitelist()
def update_content_type(name, data):
	"""Update an existing content type
	
	Args:
		name: Name of the content type
		data: Updated content type data (JSON string or dict)
		
	Returns:
		dict: Updated content type
	"""
	try:
		data = frappe.parse_json(data) if isinstance(data, str) else data
		
		# Update content type
		doc = content_type_service.update_content_type(name, data)
		return doc.as_dict()
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "CMS API Error: update_content_type")
		frappe.throw(str(e))


@frappe.whitelist()
def delete_content_type(name):
	"""Delete a content type
	
	Args:
		name: Name of the content type
		
	Returns:
		dict: Success message
	"""
	try:
		return content_type_service.delete_content_type(name)
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "CMS API Error: delete_content_type")
		frappe.throw(str(e))


@frappe.whitelist()
def add_field(content_type, field_data):
	"""Add a field to a content type
	
	Args:
		content_type: Name of the content type
		field_data: Field configuration (JSON string or dict)
		
	Returns:
		dict: Updated content type
	"""
	try:
		field_data = frappe.parse_json(field_data) if isinstance(field_data, str) else field_data
		
		# Validate field config
		field_service.validate_field_config(field_data)
		
		# Add field
		doc = field_service.add_field(content_type, field_data)
		return doc.as_dict()
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "CMS API Error: add_field")
		frappe.throw(str(e))


@frappe.whitelist()
def update_field(content_type, field_name, data):
	"""Update a field in a content type
	
	Args:
		content_type: Name of the content type
		field_name: Name of the field to update
		data: Updated field data (JSON string or dict)
		
	Returns:
		dict: Updated content type
	"""
	try:
		data = frappe.parse_json(data) if isinstance(data, str) else data
		
		# Update field
		doc = field_service.update_field(content_type, field_name, data)
		return doc.as_dict()
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "CMS API Error: update_field")
		frappe.throw(str(e))


@frappe.whitelist()
def delete_field(content_type, field_name):
	"""Delete a field from a content type
	
	Args:
		content_type: Name of the content type
		field_name: Name of the field to delete
		
	Returns:
		dict: Success message
	"""
	try:
		return field_service.delete_field(content_type, field_name)
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "CMS API Error: delete_field")
		frappe.throw(str(e))


@frappe.whitelist()
def reorder_fields(content_type, field_order):
	"""Reorder fields in a content type
	
	Args:
		content_type: Name of the content type
		field_order: List of field names in desired order (JSON string or list)
		
	Returns:
		dict: Updated content type
	"""
	try:
		field_order = frappe.parse_json(field_order) if isinstance(field_order, str) else field_order
		
		# Reorder fields
		doc = field_service.reorder_fields(content_type, field_order)
		return doc.as_dict()
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "CMS API Error: reorder_fields")
		frappe.throw(str(e))
