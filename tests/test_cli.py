"""CLI workflows and meaningful exit codes, without touching real stores."""
import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from helpdesk_lab.cli import main
from helpdesk_lab.network_diagnostics import Result


class CliTests(unittest.TestCase):
    def call(self, args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = main(args)
        return code, json.loads(output.getvalue())

    def test_full_ticket_workflow(self):
        with tempfile.TemporaryDirectory() as directory:
            base = ['--store', str(Path(directory) / 'tickets.json')]
            code, ticket = self.call(base + ['create', 'Simulated', 'Training only'])
            self.assertEqual(code, 0)
            ticket_id = ticket['id']
            self.call(base + ['update', ticket_id, '--note', 'Inspected cable', '--status', 'In Progress'])
            self.call(base + ['update', ticket_id, '--status', 'Resolved', '--resolution', 'Simulated retest successful'])
            self.call(base + ['update', ticket_id, '--status', 'Closed'])
            self.assertEqual(self.call(base + ['view', ticket_id])[1]['status'], 'Closed')
            self.assertEqual(len(self.call(base + ['list', '--status', 'Closed'])[1]), 1)

    def test_error_exit(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as error:
            main(['diagnose', 'dns'])
        self.assertEqual(error.exception.code, 2)

    def test_diagnostic_failure_exit(self):
        with patch('helpdesk_lab.cli.net.ping', return_value=Result('Ping', 'timeout', 'No response', 'Check link', False)):
            self.assertEqual(self.call(['diagnose', 'ping', 'localhost'])[0], 1)

    def test_guidance_and_kb(self):
        self.assertIn('dhcp', self.call(['diagnose', 'guidance'])[1])
        self.assertTrue(self.call(['kb', 'OneDrive'])[1])

class EntryPointTests(unittest.TestCase):
    def test_script_help_from_unrelated_directory(self):
        import subprocess
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as directory:
            for script in ('run_lab.py', 'run_network_diagnostics.py'):
                with self.subTest(script=script):
                    result = subprocess.run(
                        [sys.executable, str(root / 'scripts' / script), '--help'],
                        cwd=directory, capture_output=True, text=True,
                        timeout=10, shell=False,
                    )
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertIn('usage:', result.stdout)

    def test_invalid_destination_script_exit(self):
        import subprocess
        script = Path(__file__).resolve().parents[1] / 'scripts' / 'run_network_diagnostics.py'
        result = subprocess.run(
            [sys.executable, str(script), 'ping', 'host;command'],
            capture_output=True, text=True, timeout=10, shell=False,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn('Invalid hostname', result.stderr)
