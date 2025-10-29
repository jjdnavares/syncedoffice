# Copyright (c) 2025, jumes.dev and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import cstr


class CMSContentType(Document):
	def autoname(self):
		"""Auto-generate API ID from content type name"""
		if not self.api_id:
			self.api_id = frappe.scrub(self.content_type_name)

	def validate(self):
		"""Validate content type configuration"""
		self.validate_fields()
		self.validate_api_id()

	def validate_fields(self):
		"""Validate field configurations"""
		field_names = []
		for field in self.fields:
			# Check for duplicate field names
			if field.field_name in field_names:
				frappe.throw(f"Duplicate field name: {field.field_name}")
			field_names.append(field.field_name)

			# Validate field name format (snake_case)
			if not field.field_name.replace("_", "").isalnum():
				frappe.throw(f"Invalid field name: {field.field_name}. Use only letters, numbers, and underscores.")

	def validate_api_id(self):
		"""Ensure API ID is unique and valid"""
		if not self.api_id:
			self.api_id = frappe.scrub(self.content_type_name)

		# Check for duplicate API IDs
		existing = frappe.db.exists(
			"CMS Content Type",
			{"api_id": self.api_id, "name": ["!=", self.name]}
		)
		if existing:
			frappe.throw(f"API ID '{self.api_id}' already exists")

	def on_update(self):
		"""Handle content type updates"""
		# Clear cache for this content type
		frappe.cache().delete_value(f"cms_content_type:{self.api_id}")

	def on_trash(self):
		"""Handle content type deletion"""
		# Check if content exists for this type
		content_count = frappe.db.count("CMS Content", {"content_type": self.name})
		if content_count > 0:
			frappe.throw(
				f"Cannot delete content type. {content_count} content entries exist. "
				"Please delete all content entries first."
			)

		# Clear cache
		frappe.cache().delete_value(f"cms_content_type:{self.api_id}")
