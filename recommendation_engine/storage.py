"""JSON-backed persistence for items and user profiles."""

import json
import os
from typing import Dict, List

from models import Item, UserProfile
from exceptions import StorageError


class DataManager:
    """Handles loading and saving items/users to JSON files on disk."""

    def __init__(self, items_path: str, users_path: str):
        self.items_path = items_path
        self.users_path = users_path

    def load_items(self) -> Dict[str, Item]:
        raw = self._load_json(self.items_path)
        items: Dict[str, Item] = {}
        for entry in raw:
            try:
                item = Item.from_dict(entry)
                items[item.item_id] = item
            except (KeyError, TypeError) as exc:
                raise StorageError(f"Corrupt item record: {entry} ({exc})") from exc
        return items

    def load_users(self) -> Dict[str, UserProfile]:
        raw = self._load_json(self.users_path)
        users: Dict[str, UserProfile] = {}
        for entry in raw:
            try:
                user = UserProfile.from_dict(entry)
                users[user.user_id] = user
            except (KeyError, TypeError) as exc:
                raise StorageError(f"Corrupt user record: {entry} ({exc})") from exc
        return users

    def save_items(self, items: Dict[str, Item]) -> None:
        self._save_json(self.items_path, [item.to_dict() for item in items.values()])

    def save_users(self, users: Dict[str, UserProfile]) -> None:
        self._save_json(self.users_path, [user.to_dict() for user in users.values()])

    @staticmethod
    def _load_json(path: str) -> List[dict]:
        if not os.path.exists(path):
            return []
        try:
            with open(path, "r", encoding="utf-8") as fh:
                content = fh.read().strip()
                if not content:
                    return []
                return json.loads(content)
        except json.JSONDecodeError as exc:
            raise StorageError(f"Could not parse {path}: {exc}") from exc
        except OSError as exc:
            raise StorageError(f"Could not read {path}: {exc}") from exc

    @staticmethod
    def _save_json(path: str, data: List[dict]) -> None:
        try:
            directory = os.path.dirname(path)
            if directory:
                os.makedirs(directory, exist_ok=True)
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(data, fh, indent=2, ensure_ascii=False)
        except OSError as exc:
            raise StorageError(f"Could not write {path}: {exc}") from exc
