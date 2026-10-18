"""Search local structured support procedures."""
import json
from pathlib import Path

FIELDS = (
    'title', 'symptoms', 'questions', 'diagnostics', 'observations',
    'causes', 'resolution', 'escalation', 'record',
)


def search(path: Path, query: str = '') -> list[dict[str, str]]:
    """Match all query words across article content, case-insensitively."""
    articles = json.loads(Path(path).read_text(encoding='utf-8'))
    if not isinstance(articles, list):
        raise ValueError('Knowledge base must be a list')
    for article in articles:
        if not isinstance(article, dict) or any(
            not isinstance(article.get(key), str) or not article[key].strip()
            for key in FIELDS
        ):
            raise ValueError('Invalid knowledge base')
    words = query.lower().split()
    return [
        article for article in articles
        if all(word in ' '.join(article[key] for key in FIELDS).lower()
               for word in words)
    ]
