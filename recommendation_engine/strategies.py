"""Scoring strategies used to match users to items (Strategy design pattern).

Having an abstract base class with interchangeable subclasses lets the
engine swap the matching algorithm at runtime without changing any of
its own code (open/closed principle), and demonstrates inheritance +
polymorphism at an intermediate OOP level.
"""

from abc import ABC, abstractmethod
from typing import List, Tuple

from models import Item, UserProfile


class ScoringStrategy(ABC):
    """Base class for all recommendation scoring strategies."""

    @abstractmethod
    def score(self, item: Item, user: UserProfile) -> Tuple[float, List[str]]:
        """Return (score, matched_attributes) for this item/user pair."""
        raise NotImplementedError

    @property
    def name(self) -> str:
        return self.__class__.__name__


class JaccardSimilarityStrategy(ScoringStrategy):
    """Scores by the overlap ratio between item attributes and liked attributes.

    score = |intersection| / |union|  (classic Jaccard similarity)
    """

    def score(self, item: Item, user: UserProfile) -> Tuple[float, List[str]]:
        item_attrs = {a.lower() for a in item.attributes}
        user_attrs = {a.lower() for a in user.liked_attributes}
        if not item_attrs or not user_attrs:
            return 0.0, []
        intersection = item_attrs & user_attrs
        union = item_attrs | user_attrs
        score = len(intersection) / len(union) if union else 0.0
        return score, sorted(intersection)


class WeightedAttributeStrategy(ScoringStrategy):
    """Scores using per-attribute weights supplied in the user's profile.

    Falls back to a weight of 1.0 for liked attributes with no explicit
    weight, so a user can be set up with just `liked_attributes` too.
    """

    def score(self, item: Item, user: UserProfile) -> Tuple[float, List[str]]:
        matched: List[str] = []
        total = 0.0
        liked_lower = {a.lower() for a in user.liked_attributes}
        for attr in item.attributes:
            key = attr.lower()
            if key in user.weights:
                total += user.weights[key]
                matched.append(attr)
            elif key in liked_lower:
                total += 1.0
                matched.append(attr)
        return total, matched
