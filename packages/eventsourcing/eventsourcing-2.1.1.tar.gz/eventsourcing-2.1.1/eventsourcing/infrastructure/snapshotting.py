from abc import ABCMeta, abstractmethod

import six

from eventsourcing.domain.model.events import publish, topic_from_domain_class
from eventsourcing.domain.model.snapshot import AbstractSnapshop, Snapshot
from eventsourcing.infrastructure.eventstore import AbstractEventStore, EventStore
from eventsourcing.infrastructure.sequenceditemmapper import deserialize_domain_entity


class AbstractSnapshotStrategy(six.with_metaclass(ABCMeta)):

    @abstractmethod
    def get_snapshot(self, stored_entity_id, lt=None, lte=None):
        """Returns pre-existing snapshot for stored entity ID from given
        event store, optionally until a particular domain event ID.
        """

    @abstractmethod
    def take_snapshot(self, entity, timestamp):
        """Creates snapshot from given entity, with given domain event ID.
        """


class EventSourcedSnapshotStrategy(AbstractSnapshotStrategy):
    """Snapshot strategy that uses an event sourced snapshot.
    """
    def __init__(self, event_store):
        assert isinstance(event_store, EventStore)
        self.event_store = event_store

    def get_snapshot(self, entity_id, lt=None, lte=None):
        return get_snapshot(entity_id, self.event_store, lt=lt, lte=lte)

    def take_snapshot(self, entity, timestamp=None):
        return take_snapshot(entity, timestamp=timestamp)


def get_snapshot(entity_id, event_store, lt=None, lte=None):
    """
    Get the last snapshot for entity.

    :rtype: Snapshot
    """
    assert isinstance(event_store, AbstractEventStore)
    snapshots = event_store.get_domain_events(entity_id, lt=lt, lte=lte, is_ascending=False, limit=1)
    if len(snapshots) == 1:
        return snapshots[0]


def entity_from_snapshot(snapshot):
    """Deserialises a domain entity from a snapshot object.
    """
    assert isinstance(snapshot, AbstractSnapshop)
    return deserialize_domain_entity(snapshot.topic, snapshot.state)


def take_snapshot(entity, timestamp=None):
    # Make the 'stored entity ID' for the entity, it is used as the Snapshot 'entity ID'.

    # Create the snapshot event.
    snapshot = Snapshot(
        entity_id=entity.id,
        timestamp=timestamp,
        topic=topic_from_domain_class(entity.__class__),
        # Todo: This should be a deepcopy.
        state=entity.__dict__.copy(),
    )
    publish(snapshot)

    # Return the event.
    return snapshot
