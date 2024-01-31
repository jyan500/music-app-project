"""
	Test custom Django management commands
"""
from unittest.mock import patch
from psycopg2 import OperationalError as Psycopg2Error
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase

@patch("core.management.commands.wait_for_db.Command.check")
class CommandTests(SimpleTestCase):
	""" Test commands """
	def test_wait_for_db_ready(self, patched_check):
		""" 
			Test waiting for database if database ready
		"""
		patched_check.return_value = True
		call_command("wait_for_db")
		patched_check.assert_called_once_with(databases=["default"])

	# the patch will mock the time.sleep function so
	# it will return a None
	# so that it doesn't cause the execution of the test to halt for the sleep
	@patch("time.sleep")
	def test_wait_for_db_delay(self, patched_sleep, patched_check):
		"""
			Test waiting for database when getting OperationalError
		"""
		# the side effect allows you to pass in different types
		# and will have the appropriate response
		# the Psycopg2 * 2 means, the first two times we call the mocked method
		# we want to raise the Psycopg2 error
		# the OperationalError * 3 means, the next three times we call the mocked method,
		# we want to raise the Operational Error
		# on the 6th call, it should return True
		patched_check.side_effect = [Psycopg2Error] * 2 + \
			[OperationalError] * 3 + [True]
		call_command("wait_for_db")

		self.assertEqual(patched_check.call_count, 6)
		patched_check.assert_called_with(databases=["default"])