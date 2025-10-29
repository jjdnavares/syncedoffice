# Copyright (c) 2025, jumes.dev and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CMSComponentField(Document):
	def validate(self):
		"""Validate field configuration"""
		if not self.field_name and self.field_label:
			self.field_name = frappe.scrub(self.field_label)
