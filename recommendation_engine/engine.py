"""Core recommendation engine: item/user management and ranking logic."""

from typing import Dict, List, Optional

from models import Item, UserProfile
from strategies import ScoringStrategy
from exceptions import (
    DuplicateItemError,
    ItemNotFoundError,
    DuplicateUserError,
    UserNotFoundError,
    InvalidDataError,
)


class RecommendationEngine:
    """Owns the item/user catalogs and produces explainable recommendations."""

    def __init__(self, strategy: ScoringStrategy):
        self.items: Dict[str, Item] = {}
        self.users: Dict[str, UserProfile] = {}
        self.strategy = strategy

    def set_strategy(self, strategy: ScoringStrategy) -> None:
        self.strategy = strategy

    # ---------------- Item CRUD ----------------
    def add_item(self, item: Item) -> None:
        if not item.item_id or not item.title or not item.category:
            raise InvalidDataError("Item must have an id, a title and a category.")
        if item.item_id in self.items:
            raise DuplicateItemError(f"Item '{item.item_id}' already exists.")
        self.items[item.item_id] = item

    def remove_item(self, item_id: str) -> None:
        if item_id not in self.items:
            raise ItemNotFoundError(f"Item '{item_id}' not found.")
        del self.items[item_id]

    def find_items_by_category(self, category: str) -> List[Item]:
        return sorted(
            (i for i in self.items.values() if i.category.lower() == category.lower()),
            key=lambda i: i.title,
        )

    # ---------------- User CRUD ----------------
    def add_user(self, user: UserProfile) -> None:
        if not user.user_id or not user.name:
            raise InvalidDataError("User must have an id and a name.")
        if user.user_id in self.users:
            raise DuplicateUserError(f"User '{user.user_id}' already exists.")
        self.users[user.user_id] = user

    def get_user(self, user_id: str) -> UserProfile:
        if user_id not in self.users:
            raise UserNotFoundError(f"User '{user_id}' not found.")
        return self.users[user_id]

    # ---------------- Recommendations ----------------
    def recommend(self, user_id: str, top_n: int = 5,
                   category: Optional[str] = None) -> List[dict]:
        """Return up to top_n ranked, explainable recommendations for a user."""
        if top_n <= 0:
            raise InvalidDataError("top_n must be a positive integer.")

        user = self.get_user(user_id)
        candidates = self.items.values()
        if category:
            candidates = [i for i in candidates if i.category.lower() == category.lower()]

        scored = []
        for item in candidates:
            score, reasons = self.strategy.score(item, user)
            if score > 0:
                scored.append({"item": item, "score": round(score, 3), "reasons": reasons})

        scored.sort(key=lambda r: r["score"], reverse=True)
        return scored[:top_n]
