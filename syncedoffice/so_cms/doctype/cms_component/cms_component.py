# Copyright (c) 2025, jumes.dev and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CMSComponent(Document):
	def validate(self):
		"""Validate component configuration"""
		self.validate_fields()

	def validate_fields(self):
		"""Validate field configurations"""
		field_names = []
		for field in self.fields:
			# Check for duplicate field names
			if field.field_name in field_names:
				frappe.throw(f"Duplicate field name: {field.field_name}")
			field_names.append(field.field_name)

	def on_trash(self):
		"""Handle component deletion"""
		# Check if component is used in any content type
		# This will be implemented when we add component usage tracking
		pass
