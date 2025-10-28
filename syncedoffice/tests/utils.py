# Stub file for tests.utils module
# This is a placeholder until the full test infrastructure is implemented

import frappe
from frappe.tests import IntegrationTestCase

class SyncedOfficeTestSuite(IntegrationTestCase):
	"""Base test suite for SyncedOffice tests"""
	
	@classmethod
	def setUpClass(cls):
		"""Set up test class"""
		super().setUpClass()
	
	def setUp(self):
		"""Set up test"""
		super().setUp()
