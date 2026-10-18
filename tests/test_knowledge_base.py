"""Knowledge-base completeness and search behavior."""
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from helpdesk_lab.knowledge_base import search

KB = Path(__file__).resolve().parents[1] / 'data' / 'knowledge_base.json'


class KnowledgeTests(unittest.TestCase):
    def test_all_articles(self):
        self.assertEqual(len(search(KB)), 12)

    def test_case_insensitive_and_multiword(self):
        results = search(KB, 'DNS RESOLUTION')
        self.assertTrue(any(a['title'] == 'DNS resolution failures' for a in results))
        self.assertTrue(all('dns' in ' '.join(a.values()).lower() for a in results))

    def test_no_match(self):
        self.assertEqual(search(KB, 'unfindablezzzz'), [])

    def test_invalid_and_missing_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'kb.json'
            with self.assertRaises(FileNotFoundError):
                search(path)
            for text in ('{}', '[{}]', 'broken'):
                path.write_text(text)
                with self.assertRaises(ValueError):
                    search(path)
