class EventSourcingError(Exception):
    """Base eventsourcing exception."""


class TopicResolutionError(EventSourcingError):
    """Raised when unable to resolve a topic to a Python class."""


class EntityVersionNotFound(EventSourcingError):
    """Raise when accessing an entity version that does not exist."""


class ConcurrencyError(EventSourcingError):
    """Raised when appending events at the wrong version to a versioned stream."""


class ConsistencyError(EventSourcingError):
    """Raised when applying an event stream to a versioned entity."""


class ProgrammingError(EventSourcingError):
    """Raised when programming errors are encountered."""


class RepositoryKeyError(KeyError, EventSourcingError):
    """Raised when access an entity that does not exist."""


class SequenceFullError(EventSourcingError):
    "Raised when attempting to append an item to a sequence that is already at its maximum size."


class DatasourceSettingsError(EventSourcingError):
    "Raised when an error is detected in settings for a datasource."


class SequencedItemError(EventSourcingError):
    "Raised when an integer sequence error occurs e.g. trying to save a version that already exists."


class TimeSequenceError(EventSourcingError):
    "Raised when a time sequence error occurs e.g. trying to save a timestamp that already exists."
