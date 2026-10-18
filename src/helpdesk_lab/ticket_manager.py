"""Business rules and atomic JSON persistence, protected by a writer lock."""
import json
import os
from pathlib import Path
from typing import Callable
from .models import Ticket, required, CATEGORIES, PRIORITIES, STATUSES


class TicketManager:
    """Reject damaged stores and preserve them for manual recovery."""
    def __init__(self, path: Path) -> None:
        self.path = Path(path)

    def _read(self) -> list[Ticket]:
        if not self.path.exists():
            return []
        try:
            raw = json.loads(self.path.read_text(encoding='utf-8'))
            if not isinstance(raw, list):
                raise ValueError('Expected a JSON list')
            tickets = [Ticket(**row) for row in raw]
            if len({t.id for t in tickets}) != len(tickets):
                raise ValueError('Duplicate IDs')
            return tickets
        except (ValueError, TypeError, KeyError) as exc:
            raise ValueError(
                f'Invalid ticket store; file preserved: {exc}'
            ) from exc

    def _change(
        self, operation: Callable[[list[Ticket]], Ticket],
    ) -> Ticket:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        lock = self.path.with_suffix(self.path.suffix + '.lock')
        try:
            handle = lock.open('x')
        except FileExistsError as exc:
            raise ValueError(
                'Store busy; investigate a stale lock before removing it'
            ) from exc
        temp = self.path.with_suffix(self.path.suffix + '.tmp')
        try:
            with handle:
                tickets = self._read()
                result = operation(tickets)
                with temp.open('x', encoding='utf-8') as output:
                    json.dump([t.to_dict() for t in tickets], output, indent=2)
                    output.flush()
                    os.fsync(output.fileno())
                os.replace(temp, self.path)
                return result
        finally:
            lock.unlink()

    def create(self, **fields: str) -> Ticket:
        """Create and persist a ticket with a generated ID."""
        initial = ('title', 'description', 'category', 'priority')
        if any(key not in initial for key in fields):
            raise ValueError('Only initial ticket fields may be supplied')
        ticket = Ticket(**fields)

        def append(tickets: list[Ticket]) -> Ticket:
            tickets.append(ticket)
            return ticket

        return self._change(append)

    def list(self, **filters: str | None) -> list[Ticket]:
        """Return tickets matching every supplied filter."""
        allowed = ('status', 'category', 'priority')
        if any(key not in allowed for key in filters):
            raise ValueError('Unknown filter')
        choices = {
            'status': STATUSES, 'category': CATEGORIES, 'priority': PRIORITIES,
        }
        for key, value in filters.items():
            if value is not None and value not in choices[key]:
                raise ValueError(f'Invalid {key} filter')
        return [
            ticket for ticket in self._read()
            if all(getattr(ticket, key) == value
                   for key, value in filters.items() if value is not None)
        ]

    def get(self, ticket_id: str) -> Ticket:
        """Retrieve a ticket or raise a useful error."""
        for ticket in self._read():
            if ticket.id == ticket_id:
                return ticket
        raise ValueError('Ticket not found')

    def update(
        self, ticket_id: str, *, note: str | None = None,
        status: str | None = None, priority: str | None = None,
        resolution: str | None = None,
    ) -> Ticket:
        """Add notes, change priority or progress through the lifecycle."""
        def modify(tickets: list[Ticket]) -> Ticket:
            ticket = next(
                (t for t in tickets if t.id == ticket_id), None,
            )
            if ticket is None:
                raise ValueError('Ticket not found')
            if note is not None:
                ticket.notes.append(required(note, 'Note'))
            if priority is not None:
                if priority not in PRIORITIES:
                    raise ValueError('Invalid priority')
                ticket.priority = priority
            if resolution is not None:
                ticket.resolution = required(resolution, 'Resolution')
            if status is not None:
                if status not in STATUSES:
                    raise ValueError('Invalid status')
                if (status == 'Closed'
                        and ticket.status not in ('Resolved', 'Closed')):
                    raise ValueError('Resolve before closing')
                if (ticket.status in ('Resolved', 'Closed')
                        and status in ('Open', 'In Progress')):
                    ticket.resolution = ''
                ticket.status = status
            ticket.__post_init__()
            return ticket

        return self._change(modify)
