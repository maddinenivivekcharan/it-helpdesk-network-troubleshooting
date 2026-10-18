"""Validated, serializable ticket models."""
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from uuid import uuid4

CATEGORIES = (
    'Network', 'Hardware', 'Software', 'Account Access',
    'Microsoft 365', 'Security',
)
PRIORITIES = ('Low', 'Medium', 'High', 'Critical')
STATUSES = ('Open', 'In Progress', 'Resolved', 'Closed')


def required(value: str, name: str) -> str:
    """Require bounded text; callers must redact sensitive information."""
    if not isinstance(value, str) or not value.strip() or len(value) > 4000:
        raise ValueError(f'{name} must contain 1-4000 characters')
    return value.strip()


@dataclass
class Ticket:
    """A simulated support request, without identity fields."""
    title: str
    description: str
    category: str = 'Network'
    priority: str = 'Medium'
    status: str = 'Open'
    id: str = field(default_factory=lambda: 'LAB-' + uuid4().hex)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    notes: list[str] = field(default_factory=list)
    resolution: str = ''

    def __post_init__(self) -> None:
        self.title = required(self.title, 'Title')
        self.description = required(self.description, 'Description')
        required(self.id, 'ID')
        timestamp = datetime.fromisoformat(self.created_at)
        if timestamp.tzinfo is None:
            raise ValueError('Creation time must include a timezone')
        if (self.category not in CATEGORIES
                or self.priority not in PRIORITIES
                or self.status not in STATUSES):
            raise ValueError('Invalid category, priority, or status')
        if not isinstance(self.notes, list):
            raise ValueError('Notes must be a list')
        for note in self.notes:
            required(note, 'Note')
        if not isinstance(self.resolution, str):
            raise ValueError('Resolution must be text')
        if self.status in ('Resolved', 'Closed'):
            required(self.resolution, 'Resolution')

    def to_dict(self) -> dict:
        """Return a JSON-compatible record."""
        return asdict(self)
