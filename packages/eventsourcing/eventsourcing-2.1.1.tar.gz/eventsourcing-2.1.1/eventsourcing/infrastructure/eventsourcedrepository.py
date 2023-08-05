from abc import abstractproperty

from eventsourcing.domain.model.entity import AbstractEntityRepository
from eventsourcing.exceptions import RepositoryKeyError
from eventsourcing.infrastructure.eventplayer import EventPlayer
from eventsourcing.infrastructure.eventstore import AbstractEventStore
from eventsourcing.infrastructure.snapshotting import entity_from_snapshot


class EventSourcedRepository(AbstractEntityRepository):

    # If the entity won't have very many events, marking the entity as
    # "short" by setting __is_short__ value equal to True will mean
    # the fastest path for getting all the events is used. If you set
    # a value for page size (see below), this option will have no effect.
    __is_short__ = False

    # The page size by which events are retrieved. If this
    # value is set to a positive integer, the events of
    # the entity will be retrieved in pages, using a series
    # of queries, rather than with one potentially large query.
    __page_size__ = None

    # The mutator function used by this repository. Can either
    # be set as a class attribute, or passed as a constructor arg.
    mutator = None

    def __init__(self, event_store, mutator=None, snapshot_strategy=None, use_cache=False):
        self._cache = {}
        self._snapshot_strategy = snapshot_strategy
        # self._use_cache = use_cache

        # Check we got an event store.
        assert isinstance(event_store, AbstractEventStore)
        self.event_store = event_store

        # Instantiate an event player for this repo.
        mutator = mutator or type(self).mutator
        if mutator is None:
            raise ValueError("Repository needs a mutator function (set class attribute or pass constructor arg)")
        self.event_player = EventPlayer(
            event_store=self.event_store,
            mutator=mutator,
            page_size=self.__page_size__,
            is_short=self.__is_short__,
            snapshot_strategy=self._snapshot_strategy,
        )

    def __contains__(self, entity_id):
        """
        Returns a boolean value according to whether entity with given ID exists.
        """
        return self.get_entity(entity_id) is not None

    def __getitem__(self, entity_id):
        """
        Returns entity with given ID.
        """
        # # Get entity from the cache.
        # if self._use_cache:
        #     try:
        #         return self._cache[entity_id]
        #     except KeyError:
        #         pass

        # Reconstitute the entity.
        entity = self.get_entity(entity_id)

        # Never created or already discarded?
        if entity is None:
            raise RepositoryKeyError(entity_id)

        # # Put entity in the cache.
        # if self._use_cache:
        #     self.add_cache(entity_id, entity)

        # Return entity.
        return entity

    # def add_cache(self, entity_id, entity):
    #     self._cache[entity_id] = entity

    def get_entity(self, entity_id, lte=None):
        """
        Returns entity with given ID, optionally as it was until the given domain event ID.
        """

        # Get a snapshot (None if none exist).
        if self._snapshot_strategy is not None:
            snapshot = self._snapshot_strategy.get_snapshot(entity_id, lte=lte)
        else:
            snapshot = None

        # Decide the initial state, and after when we need to get the events.
        if snapshot is None:
            initial_state = None
            gte = None
        else:
            initial_state = entity_from_snapshot(snapshot)
            gte = initial_state._version

        # Replay domain events.
        return self.event_player.replay_entity(entity_id, gte=gte, lte=lte, initial_state=initial_state)

    # def fastforward(self, stale_entity, lt=None, lte=None):
    #     """
    #     Mutates an instance of an entity, according to the events that have occurred since its version.
    #     """
    #     return self.event_player.fastforward(stale_entity, lt=lt, lte=lte)
