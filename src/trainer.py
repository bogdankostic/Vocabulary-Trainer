from typing import Tuple, Optional
from datetime import datetime, timedelta
from itertools import chain

from src.models import User, WordPair


def add_user(users: Tuple[User, ...], user_name: str) -> Tuple[User, ...]:
    new_user = User(name=user_name, word_pairs=())
    return users + (new_user,)


def add_word_pair(user: User, word_a: str, word_b: str, category: str) -> User:
    new_word_pair = WordPair(word_a=word_a, word_b=word_b, category=category, last_practiced=None)
    updated_word_pairs = user.word_pairs + (new_word_pair,)
    return User(name=user.name, word_pairs=updated_word_pairs)


def get_word_pairs(user: User) -> Tuple[WordPair, ...]:
    return user.word_pairs


def get_word_pairs_by_category(user: User, category: str) -> Tuple[WordPair, ...]:
    return tuple(filter(lambda wp: wp.category == category, user.word_pairs))


def get_word_pairs_to_practice(user: User, categories: Optional[Tuple[str, ...]] = None) -> Tuple[WordPair, ...]:
    if categories is not None:
        word_pairs = tuple(chain.from_iterable(get_word_pairs_by_category(user, category) for category in categories))
    else:
        word_pairs = get_word_pairs(user)

    return tuple(filter(is_due_for_practice, word_pairs))


def is_due_for_practice(word_pair: WordPair) -> bool:
    # word pair has never been practiced
    if word_pair.last_practiced is None:
        return True

    # word pair has been last practiced more than 3 months ago
    three_months_ago = datetime.now() - timedelta(days=90)
    if word_pair.last_practiced < three_months_ago:
        return True

    # word pair has been last practiced more than 1 week ago and was correctly answered for less than 3 times
    one_week_ago = datetime.now() - timedelta(days=7)
    if word_pair.last_practiced < one_week_ago and word_pair.num_correctly_answered < 3:
        return True

    # word pair has been correctly answered for 3 times in the last three months
    return False
