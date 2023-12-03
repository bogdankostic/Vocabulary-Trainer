from typing import NamedTuple, Tuple, Optional
from datetime import datetime


class User(NamedTuple):
    name: str
    word_pairs: Tuple["WordPair", ...]


class WordPair(NamedTuple):
    word_a: str
    word_b: str
    category: str = "uncategorized"
    last_practiced: Optional[datetime] = None
    num_correctly_answered: int = 0

