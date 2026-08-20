"""Custom exceptions for the Simple Recommendation Engine project."""


class RecommendationEngineError(Exception):
    """Base exception for this application."""


class DuplicateItemError(RecommendationEngineError):
    """Raised when an item with an already-used ID is added."""


class ItemNotFoundError(RecommendationEngineError):
    """Raised when a referenced item does not exist."""


class DuplicateUserError(RecommendationEngineError):
    """Raised when a user with an already-used ID is added."""


class UserNotFoundError(RecommendationEngineError):
    """Raised when a referenced user does not exist."""


class InvalidDataError(RecommendationEngineError):
    """Raised when input data fails validation."""


class StorageError(RecommendationEngineError):
    """Raised when reading or writing persisted data fails."""
