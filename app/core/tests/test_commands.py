from unittest import mock

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class WaitForDBTest(TestCase):

    def test_waite_for_db_ready(self):
        """Test waiting for db when it's available."""
        with mock.patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.return_value = True
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 1)

    @mock.patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """Test wait for db."""
        with mock.patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.side_effect = [OperationalError] * 5 + [True, ]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)
