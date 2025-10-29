# Copyright (c) 2025, jumes.dev and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CMSContentTypeField(Document):
	def validate(self):
		"""Validate field configuration"""
		self.validate_field_name()
		self.validate_field_type_options()

	def validate_field_name(self):
		"""Ensure field name is in snake_case format"""
		if not self.field_name:
			return

		# Convert to snake_case if not already
		if not self.field_name.replace("_", "").isalnum():
			frappe.throw(f"Invalid field name: {self.field_name}. Use only letters, numbers, and underscores.")

		# Auto-generate from label if empty
		if not self.field_name and self.field_label:
			self.field_name = frappe.scrub(self.field_label)

	def validate_field_type_options(self):
		"""Validate field type specific options"""
		if self.field_type == "Relation" and self.options:
			# Validate relation options
			options = frappe.parse_json(self.options) if isinstance(self.options, str) else self.options
			if not options.get("target"):
				frappe.throw("Relation field must specify a target content type in options")

		elif self.field_type == "Component" and self.options:
			# Validate component options
			options = frappe.parse_json(self.options) if isinstance(self.options, str) else self.options
			if not options.get("component"):
				frappe.throw("Component field must specify a component reference in options")

		elif self.field_type == "Enumeration" and self.options:
			# Validate enumeration options
			options = frappe.parse_json(self.options) if isinstance(self.options, str) else self.options
			if not options.get("values"):
				frappe.throw("Enumeration field must specify values in options")
