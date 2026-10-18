"""Offline diagnostics tests; no live DNS, ICMP or commands."""
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from helpdesk_lab import network_diagnostics as net


class NetworkTests(unittest.TestCase):
    def runner(self, code=0):
        return Mock(return_value=subprocess.CompletedProcess([], code, 'simulated output', ''))

    def test_host_validation(self):
        for host in ('localhost', 'example.test', '127.0.0.1', '::1', 'host-name.'):
            self.assertEqual(net.validate_host(host), host)
        for host in ('', '-n', 'x;whoami', 'x y', 'https://example.test', 'a/b', 'a..b', 'a' * 64, 'fe80::1%eth0'):
            with self.subTest(host=host), self.assertRaises(ValueError):
                net.validate_host(host)

    def test_windows_ping_arguments(self):
        runner = self.runner()
        result = net.ping('127.0.0.1', runner, 'Windows')
        self.assertTrue(result.ok)
        args, kwargs = runner.call_args
        self.assertEqual(args[0], ['ping', '-n', '2', '-w', '1000', '127.0.0.1'])
        self.assertFalse(kwargs['shell'])
        self.assertEqual(kwargs['timeout'], 8)
        self.assertIn('ICMP', result.meaning)

    def test_unix_ping_and_failed_exit(self):
        for system in ('Linux', 'Darwin'):
            runner = self.runner(1)
            result = net.ping('localhost', runner, system)
            self.assertFalse(result.ok)
            self.assertEqual(runner.call_args.args[0], ['ping', '-c', '2', 'localhost'])
            self.assertIn('Exit 1', result.result)

    def test_missing_permission_and_timeout(self):
        for error in (FileNotFoundError('missing'), PermissionError('denied'), subprocess.TimeoutExpired('ping', 8)):
            result = net.ping('localhost', Mock(side_effect=error), 'Windows')
            self.assertFalse(result.ok)
            self.assertTrue(result.next_step)

    def test_unsupported_os_does_not_execute(self):
        runner = self.runner()
        self.assertFalse(net.ping('localhost', runner, 'Unknown').ok)
        self.assertFalse(net.ip_configuration(runner, 'Unknown').ok)
        runner.assert_not_called()

    def test_invalid_host_does_not_execute(self):
        runner = self.runner()
        with self.assertRaises(ValueError):
            net.ping('-n 500', runner, 'Windows')
        runner.assert_not_called()

    def test_configuration_commands(self):
        for system, command in [('Windows', ['ipconfig', '/all']), ('Linux', ['ip', 'address']), ('Darwin', ['ifconfig'])]:
            runner = self.runner()
            self.assertTrue(net.ip_configuration(runner, system).ok)
            self.assertEqual(runner.call_args.args[0], command)

    def test_dns_success_does_not_claim_internet(self):
        resolver = Mock(return_value=['192.0.2.1'])
        result = net.resolve('example.test', resolver)
        self.assertTrue(result.ok)
        self.assertIn('does not prove internet', result.meaning)
        resolver.assert_called_once_with('example.test', 4)

    def test_dns_error_timeout_and_empty(self):
        for resolver in (Mock(side_effect=OSError('not found')), Mock(side_effect=subprocess.TimeoutExpired('dns', 4)), Mock(return_value=[])):
            self.assertFalse(net.resolve('example.test', resolver).ok)

    def test_real_resolver_wrapper_mocked_process(self):
        with patch.object(net.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, '["192.0.2.1"]', '')) as run:
            self.assertEqual(net._system_resolver('example.test', 2), ['192.0.2.1'])
            self.assertEqual(run.call_args.kwargs['timeout'], 2)
            self.assertFalse(run.call_args.kwargs['shell'])
        with patch.object(net.subprocess, 'run', return_value=subprocess.CompletedProcess([], 1, '', '')):
            self.assertFalse(net.resolve('example.test').ok)

    def test_hostname_success_and_error(self):
        with patch.object(net.socket, 'gethostname', return_value='training-device'):
            self.assertEqual(net.local_hostname().result, 'training-device')
        with patch.object(net.socket, 'gethostname', side_effect=OSError('unavailable')):
            self.assertFalse(net.local_hostname().ok)
