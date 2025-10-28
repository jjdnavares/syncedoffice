# Stub file for transaction_base module
# This is a placeholder until the full utilities module is implemented

import frappe
from frappe.model.document import Document

class TransactionBase(Document):
	"""Base class for transaction documents"""
	
	def set_missing_values(self, for_validate=False):
		"""Stub method for setting missing values"""
		pass
	
	def calculate_taxes_and_totals(self):
		"""Stub method for calculating taxes and totals"""
		pass
