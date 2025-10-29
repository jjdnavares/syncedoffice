# Copyright (c) 2025, jumes.dev and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import now_datetime


class CMSContent(Document):
	def before_insert(self):
		"""Set created by user"""
		self.created_by_user = frappe.session.user

	def validate(self):
		"""Validate content data against content type schema"""
		self.modified_by_user = frappe.session.user
		self.validate_content_data()

	def validate_content_data(self):
		"""Validate content data against content type fields"""
		if not self.content_type:
			return

		# Get content type definition
		content_type = frappe.get_doc("CMS Content Type", self.content_type)
		
		# Parse content data
		content_data = frappe.parse_json(self.content_data) if isinstance(self.content_data, str) else (self.content_data or {})

		# Validate required fields
		for field in content_type.fields:
			if field.required and not content_data.get(field.field_name):
				frappe.throw(_(f"Field '{field.field_label}' is required"))

			# Validate unique fields
			if field.unique and content_data.get(field.field_name):
				self.validate_unique_field(field.field_name, content_data.get(field.field_name))

	def validate_unique_field(self, field_name, value):
		"""Check if field value is unique"""
		filters = {
			"content_type": self.content_type,
			"name": ["!=", self.name] if not self.is_new() else ["is", "set"]
		}
		
		# Query for existing content with same field value
		existing = frappe.get_all(
			"CMS Content",
			filters=filters,
			fields=["name", "content_data"]
		)

		for doc in existing:
			existing_data = frappe.parse_json(doc.content_data) if isinstance(doc.content_data, str) else (doc.content_data or {})
			if existing_data.get(field_name) == value:
				frappe.throw(_(f"Value '{value}' for field '{field_name}' already exists"))

	def on_update(self):
		"""Handle content updates"""
		# Update published_at when status changes to Published
		if self.status == "Published" and not self.published_at:
			self.db_set("published_at", now_datetime(), update_modified=False)

	def before_save(self):
		"""Clear published_at if status is Draft"""
		if self.status == "Draft":
			self.published_at = None
