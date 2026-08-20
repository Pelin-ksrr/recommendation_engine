"""Data models for the Simple Recommendation Engine project."""

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class Item:
    """Represents a recommendable item (e.g., a book or a movie)."""

    item_id: str
    title: str
    category: str
    attributes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "item_id": self.item_id,
            "title": self.title,
            "category": self.category,
            "attributes": self.attributes,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Item":
        return Item(
            item_id=data["item_id"],
            title=data["title"],
            category=data["category"],
            attributes=list(data.get("attributes", [])),
        )


@dataclass
class UserProfile:
    """Represents a user and the attributes they are interested in."""

    user_id: str
    name: str
    liked_attributes: List[str] = field(default_factory=list)
    weights: Dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "name": self.name,
            "liked_attributes": self.liked_attributes,
            "weights": self.weights,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "UserProfile":
        return UserProfile(
            user_id=data["user_id"],
            name=data["name"],
            liked_attributes=list(data.get("liked_attributes", [])),
            weights=dict(data.get("weights", {})),
        )
