"""CLI interaction, separate from diagnostics and ticket business rules."""
import argparse
import json
from pathlib import Path
from .models import CATEGORIES, PRIORITIES, STATUSES
from .ticket_manager import TicketManager
from .knowledge_base import search
from . import network_diagnostics as net

ROOT = Path(__file__).resolve().parents[2]


def build_parser() -> argparse.ArgumentParser:
    """Define commands and validate enumerated options."""
    parser = argparse.ArgumentParser(
        description=(
            'Simulated IT support lab. '
            'Never enter secrets or personal information.'
        )
    )
    parser.add_argument(
        '--store', type=Path,
        default=Path.home() / '.helpdesk_lab' / 'tickets.json',
        help='Live JSON store; specify before the subcommand',
    )
    commands = parser.add_subparsers(dest='command', required=True)
    create = commands.add_parser('create', help='Create a simulated ticket')
    create.add_argument('title')
    create.add_argument('description')
    create.add_argument('--category', choices=CATEGORIES, default='Network')
    create.add_argument('--priority', choices=PRIORITIES, default='Medium')
    listing = commands.add_parser('list', help='List and filter tickets')
    for name, choices in (
        ('status', STATUSES), ('category', CATEGORIES),
        ('priority', PRIORITIES),
    ):
        listing.add_argument('--' + name, choices=choices)
    view = commands.add_parser('view', help='View one ticket by ID')
    view.add_argument('id')
    update = commands.add_parser(
        'update', help='Record investigation/progress'
    )
    update.add_argument('id')
    update.add_argument('--note')
    update.add_argument('--status', choices=STATUSES)
    update.add_argument('--priority', choices=PRIORITIES)
    update.add_argument('--resolution')
    kb = commands.add_parser('kb', help='Search local support procedures')
    kb.add_argument('query', nargs='?', default='')
    kb.add_argument(
        '--file', type=Path, default=ROOT / 'data' / 'knowledge_base.json'
    )
    diag = commands.add_parser('diagnose', help='Run a bounded safe check')
    diag.add_argument(
        'check', choices=['hostname', 'dns', 'ping', 'ip', 'guidance']
    )
    diag.add_argument('host', nargs='?')
    return parser


def main(argv: list[str] | None = None) -> int:
    """Return 0 success, 1 diagnostic failure, 2 input/storage error."""
    parser = build_parser()
    args = parser.parse_args(argv)
    manager = TicketManager(args.store)
    try:
        if args.command == 'create':
            result = manager.create(
                title=args.title, description=args.description,
                category=args.category, priority=args.priority,
            ).to_dict()
        elif args.command == 'list':
            result = [t.to_dict() for t in manager.list(
                status=args.status, category=args.category,
                priority=args.priority,
            )]
        elif args.command == 'view':
            result = manager.get(args.id).to_dict()
        elif args.command == 'update':
            fields = ('note', 'status', 'priority', 'resolution')
            if all(getattr(args, field) is None for field in fields):
                raise ValueError('Specify at least one update option')
            result = manager.update(
                args.id, note=args.note, status=args.status,
                priority=args.priority, resolution=args.resolution,
            ).to_dict()
        elif args.command == 'kb':
            result = search(args.file, args.query)
        else:
            if args.check in ('dns', 'ping') and not args.host:
                raise ValueError('DNS and ping require a hostname or IP')
            checks = {
                'hostname': lambda: net.local_hostname().to_dict(),
                'dns': lambda: net.resolve(args.host).to_dict(),
                'ping': lambda: net.ping(args.host).to_dict(),
                'ip': lambda: net.ip_configuration().to_dict(),
                'guidance': lambda: net.GUIDANCE,
            }
            result = checks[args.check]()
        print(json.dumps(result, indent=2))
        failed = isinstance(result, dict) and result.get('ok') is False
        return 1 if failed else 0
    except (ValueError, OSError, TypeError) as exc:
        parser.exit(2, f'Error: {exc}\n')


if __name__ == '__main__':
    raise SystemExit(main())
