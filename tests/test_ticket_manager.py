"""Storage integrity and ticket lifecycle tests in isolated temporary directories."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from helpdesk_lab.ticket_manager import TicketManager


class TicketTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'tickets.json'
        self.manager = TicketManager(self.path)

    def create(self, **kwargs):
        return self.manager.create(title='Simulated outage', description='Training only', **kwargs)

    def test_missing_store_and_persistence(self):
        self.assertEqual(self.manager.list(), [])
        ticket = self.create()
        self.assertEqual(TicketManager(self.path).get(ticket.id), ticket)
        self.assertEqual(len(json.loads(self.path.read_text())), 1)

    def test_filters_combine(self):
        self.create(priority='High')
        second = self.create(category='Hardware', priority='Low')
        self.assertEqual(self.manager.list(category='Hardware', priority='Low'), [second])
        self.assertEqual(self.manager.list(status='Resolved'), [])
        with self.assertRaises(ValueError):
            self.manager.list(unknown='x')
        with self.assertRaises(ValueError):
            self.manager.list(priority='Urgent')

    def test_lifecycle_notes_priority_and_reopen(self):
        ticket = self.create()
        self.manager.update(ticket.id, note='Cable inspected', status='In Progress', priority='High')
        self.assertEqual(self.manager.get(ticket.id).notes, ['Cable inspected'])
        self.assertEqual(self.manager.get(ticket.id).priority, 'High')
        self.manager.update(ticket.id, status='Resolved', resolution='Simulated cable reconnected; test works')
        self.manager.update(ticket.id, status='Closed')
        reopened = self.manager.update(ticket.id, status='Open')
        self.assertEqual(reopened.resolution, '')
        self.assertEqual(reopened.status, 'Open')

    def test_invalid_update_preserves_bytes(self):
        ticket = self.create()
        before = self.path.read_bytes()
        for fields in ({'status': 'Resolved'}, {'status': 'Closed'}, {'note': ' '},
                       {'priority': 'Wrong'}, {'status': 'Wrong'}, {'resolution': ' '}):
            with self.subTest(fields=fields), self.assertRaises(ValueError):
                self.manager.update(ticket.id, **fields)
            self.assertEqual(self.path.read_bytes(), before)

    def test_missing_ticket(self):
        with self.assertRaises(ValueError):
            self.manager.get('missing')
        with self.assertRaises(ValueError):
            self.manager.update('missing', note='Training')

    def test_corrupt_stores_preserved(self):
        for content in ('{broken', '{}', '[{}]', '[42]'):
            self.path.write_text(content, encoding='utf-8')
            with self.subTest(content=content), self.assertRaises(ValueError):
                self.create()
            self.assertEqual(self.path.read_text(), content)

    def test_duplicate_ids_rejected(self):
        ticket = self.create().to_dict()
        self.path.write_text(json.dumps([ticket, ticket]))
        with self.assertRaises(ValueError):
            self.manager.list()

    def test_lock_prevents_write(self):
        self.path.with_suffix('.json.lock').write_text('')
        with self.assertRaises(ValueError):
            self.create()
        self.assertFalse(self.path.exists())

    def test_replace_failure_preserves_existing_store(self):
        ticket = self.create()
        before = self.path.read_bytes()
        with patch('helpdesk_lab.ticket_manager.os.replace', side_effect=PermissionError('Denied')):
            with self.assertRaises(PermissionError):
                self.manager.update(ticket.id, note='Training')
        self.assertEqual(self.path.read_bytes(), before)
        self.assertTrue(self.path.with_suffix('.json.tmp').exists())
        # Stale temp blocks new writes rather than silently overwriting recovery data.
        with self.assertRaises(FileExistsError):
            self.create()

    def test_creation_cannot_supply_id_or_resolved_state(self):
        for extra in ({'id': 'fixed'}, {'status': 'Resolved'}):
            with self.assertRaises(ValueError):
                self.create(**extra)

    def test_sample_store_valid(self):
        samples = Path(__file__).resolve().parents[1] / 'data' / 'sample_tickets.json'
        self.assertEqual(len(TicketManager(samples).list()), 3)
