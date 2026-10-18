"""Bounded read-only commands with injectable system interfaces."""
import ipaddress
import json
import platform
import re
import socket
import subprocess
import sys
from dataclasses import dataclass, asdict
from typing import Callable

Runner = Callable[..., subprocess.CompletedProcess[str]]
Resolver = Callable[[str, float], list[str]]


@dataclass
class Result:
    """Keep actual evidence separate from interpretation and next steps."""
    name: str
    result: str
    meaning: str
    next_step: str
    ok: bool = True

    def to_dict(self) -> dict:
        """Return a record suitable for CLI JSON output."""
        return asdict(self)


def validate_host(host: str) -> str:
    """Accept literal IPs or ASCII DNS names; reject flags and shell text."""
    if (not isinstance(host, str) or not host
            or len(host) > 253 or '%' in host):
        raise ValueError('Provide a hostname or IP, without a zone identifier')
    try:
        ipaddress.ip_address(host)
        return host
    except ValueError:
        pass
    labels = host.rstrip('.').split('.')
    pattern = r'[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?'
    if not all(re.fullmatch(pattern, label) for label in labels):
        raise ValueError(
            'Invalid hostname; URLs and command arguments are forbidden'
        )
    return host


def local_hostname() -> Result:
    """Read the local host label without accessing a remote host."""
    try:
        return Result(
            'Hostname', socket.gethostname(), 'Local host label only.',
            'Compare with your lab inventory.',
        )
    except OSError as exc:
        return Result(
            'Hostname', str(exc), 'Lookup failed.',
            'Inspect OS availability.', False,
        )


def _system_resolver(host: str, timeout: float) -> list[str]:
    # getaddrinfo has no portable deadline; a child process can be terminated.
    code = (
        'import socket,json,sys; print(json.dumps(sorted({r[4][0] '
        'for r in socket.getaddrinfo(sys.argv[1],None)})))'
    )
    completed = subprocess.run(
        [sys.executable, '-c', code, host], capture_output=True,
        text=True, timeout=timeout, shell=False,
    )
    if completed.returncode:
        details = completed.stderr.strip().splitlines()
        raise OSError(
            details[-1] if details else 'System resolver failed'
        )
    return json.loads(completed.stdout)


def resolve(
    host: str, resolver: Resolver = _system_resolver, timeout: float = 4,
) -> Result:
    """Resolve through the OS; injected resolvers receive host and timeout."""
    host = validate_host(host)
    try:
        addresses = resolver(host, timeout)
        if not addresses:
            raise OSError('No addresses returned')
        return Result(
            'DNS', ', '.join(addresses),
            'Addresses returned; this does not prove internet access.',
            'Compare with the expected service address.',
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return Result(
            'DNS', str(exc), 'Resolution failed or timed out.',
            'Check configured DNS and an approved known hostname.', False,
        )


def _command(
    name: str, args: list[str], runner: Runner,
    meaning: str, next_step: str,
) -> Result:
    try:
        completed = runner(
            args, capture_output=True, text=True, timeout=8,
            shell=False, errors='replace',
        )
        actual = (
            f'Exit {completed.returncode}\n'
            f'{completed.stdout}\n{completed.stderr}'
        ).strip()
        return Result(
            name, actual, meaning, next_step, completed.returncode == 0,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return Result(
            name, str(exc), 'Command unavailable, denied, or timed out.',
            'Check command installation and permissions; '
            'do not elevate automatically.', False,
        )


def ping(
    host: str, runner: Runner = subprocess.run, system: str | None = None,
) -> Result:
    """Send exactly two ICMP requests with an outer process deadline."""
    host = validate_host(host)
    system = system or platform.system()
    if system == 'Windows':
        args = ['ping', '-n', '2', '-w', '1000', host]
    elif system in ('Linux', 'Darwin'):
        args = ['ping', '-c', '2', host]
    else:
        return Result(
            'Ping', 'Unsupported OS', 'No command executed.',
            'Inspect OS documentation.', False,
        )
    return _command(
        'Ping', args, runner,
        'Inspect replies and exit code. ICMP may be blocked while a service '
        'works; some Windows failures can return zero.',
        'Compare your gateway and the application itself.',
    )


def ip_configuration(
    runner: Runner = subprocess.run, system: str | None = None,
) -> Result:
    """Display local configuration without changing it or saving output."""
    system = system or platform.system()
    commands = {
        'Windows': ['ipconfig', '/all'],
        'Linux': ['ip', 'address'],
        'Darwin': ['ifconfig'],
    }
    if system not in commands:
        return Result(
            'IP configuration', 'Unsupported OS', 'No command executed.',
            'Inspect settings manually.', False,
        )
    return _command(
        'IP configuration', commands[system], runner,
        'Local configuration only; may contain device identifiers.',
        'Inspect address, gateway and DNS locally. Redact before sharing; '
        'never store raw output in tickets.',
    )


GUIDANCE = {
    'gateway': (
        'Inspect the default route. Test only your own gateway if authorized; '
        'ICMP filtering can hide replies.'
    ),
    'dns': (
        'Compare a known hostname and expected address. '
        'DNS success does not prove application connectivity.'
    ),
    'dhcp': (
        '169.254.x.x often indicates no IPv4 DHCP lease. '
        'Check link and consult authorized DHCP support.'
    ),
    'wifi': (
        'Check airplane mode, signal, correct SSID and captive portal. '
        'Never disclose credentials.'
    ),
}
