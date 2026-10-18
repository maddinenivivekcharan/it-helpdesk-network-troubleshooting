"""Model invariants independent of persistence."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from helpdesk_lab.models import Ticket


class ModelTests(unittest.TestCase):
    def test_defaults_and_unique_ids(self):
        first, second = Ticket('Lab', 'Simulated'), Ticket('Lab', 'Simulated')
        self.assertNotEqual(first.id, second.id)
        self.assertEqual(first.status, 'Open')
        self.assertIn('+00:00', first.created_at)
        self.assertEqual(Ticket(**first.to_dict()), first)

    def test_invalid_inputs(self):
        for fields in ({'title': ' '}, {'description': None}, {'category': 'Other'},
                       {'priority': 'Urgent'}, {'status': 'Done'}, {'notes': 'bad'},
                       {'notes': ['']}, {'created_at': 'yesterday'},
                       {'created_at': '2026-01-01'}, {'resolution': 42},
                       {'title': 'x' * 4001}):
            with self.subTest(fields=fields), self.assertRaises((ValueError, TypeError)):
                Ticket(**({'title': 'Lab', 'description': 'Simulated'} | fields))

    def test_resolution_required_for_finished_ticket(self):
        for status in ('Resolved', 'Closed'):
            with self.subTest(status=status), self.assertRaises(ValueError):
                Ticket('Lab', 'Simulated', status=status)
