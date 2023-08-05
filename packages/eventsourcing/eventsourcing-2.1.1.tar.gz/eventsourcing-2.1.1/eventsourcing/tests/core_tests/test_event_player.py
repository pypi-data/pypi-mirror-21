from uuid import uuid4

from eventsourcing.application.policies import CombinedPersistencePolicy
from eventsourcing.domain.model.events import assert_event_handlers_empty
from eventsourcing.example.domainmodel import Example, register_new_example
from eventsourcing.infrastructure.eventplayer import EventPlayer
from eventsourcing.infrastructure.eventstore import EventStore
from eventsourcing.infrastructure.sequenceditem import SequencedItem
from eventsourcing.infrastructure.snapshotting import entity_from_snapshot, EventSourcedSnapshotStrategy
from eventsourcing.infrastructure.sqlalchemy.activerecords import SQLAlchemyActiveRecordStrategy, \
    SqlIntegerSequencedItem, SqlTimestampSequencedItem
from eventsourcing.infrastructure.sequenceditemmapper import SequencedItemMapper
from eventsourcing.tests.datastore_tests.test_sqlalchemy import SQLAlchemyDatastoreTestCase


class TestEventPlayer(SQLAlchemyDatastoreTestCase):
    def setUp(self):
        assert_event_handlers_empty()
        super(TestEventPlayer, self).setUp()

        self.datastore.setup_connection()
        self.datastore.setup_tables()

        # Setup an event store for version entity events.
        self.version_entity_event_store = EventStore(
            active_record_strategy=SQLAlchemyActiveRecordStrategy(
                datastore=self.datastore,
                active_record_class=SqlIntegerSequencedItem,
                sequenced_item_class=SequencedItem,
            ),
            sequenced_item_mapper=SequencedItemMapper(
                sequenced_item_class=SequencedItem,
                event_sequence_id_attr='entity_id',
                event_position_attr='entity_version',
            ),
        )

        # Setup an event store for timestamp entity events.
        self.timestamp_entity_event_store = EventStore(
            active_record_strategy=SQLAlchemyActiveRecordStrategy(
                datastore=self.datastore,
                active_record_class=SqlTimestampSequencedItem,
                sequenced_item_class=SequencedItem,
            ),
            sequenced_item_mapper=SequencedItemMapper(
                sequenced_item_class=SequencedItem,
                event_sequence_id_attr='entity_id',
                event_position_attr='timestamp',
            ),
        )

        self.policy = None

    def tearDown(self):
        self.datastore.drop_tables()
        self.datastore.drop_connection()
        if self.policy is not None:
            self.policy.close()
        super(TestEventPlayer, self).tearDown()
        assert_event_handlers_empty()

    def test_get_entity(self):
        # Store example events.
        entity_id1 = uuid4()
        event1 = Example.Created(entity_id=entity_id1, a=1, b=2)
        self.version_entity_event_store.append(event1)
        entity_id2 = uuid4()
        event2 = Example.Created(entity_id=entity_id2, a=2, b=4)
        self.version_entity_event_store.append(event2)
        entity_id3 = uuid4()
        event3 = Example.Created(entity_id=entity_id3, a=3, b=6)
        self.version_entity_event_store.append(event3)
        event4 = Example.Discarded(entity_id=entity_id3, entity_version=1)
        self.version_entity_event_store.append(event4)

        # Check the event sourced entities are correct.
        # - just use a trivial mutate that always instantiates the 'Example'.
        event_player = EventPlayer(event_store=self.version_entity_event_store, mutator=Example.mutate)

        # The the reconstituted entity has correct attribute values.
        self.assertEqual(entity_id1, event_player.replay_entity(entity_id1).id)
        self.assertEqual(1, event_player.replay_entity(entity_id1).a)
        self.assertEqual(2, event_player.replay_entity(entity_id2).a)
        self.assertEqual(None, event_player.replay_entity(entity_id3))

        # Check entity3 raises KeyError.
        self.assertEqual(event_player.replay_entity(entity_id3), None)

        # Check it works for "short" entities (should be faster, but the main thing is that it still works).
        # - just use a trivial mutate that always instantiates the 'Example'.
        event5 = Example.AttributeChanged(entity_id=entity_id1, entity_version=1, name='a', value=10)
        self.version_entity_event_store.append(event5)

        event_player = EventPlayer(event_store=self.version_entity_event_store, mutator=Example.mutate)
        self.assertEqual(10, event_player.replay_entity(entity_id1).a)

        event_player = EventPlayer(
            event_store=self.version_entity_event_store,
            mutator=Example.mutate,
            is_short=True,
        )
        self.assertEqual(10, event_player.replay_entity(entity_id1).a)

    # Todo: Maybe this is an application-level test? If not, test event player capabilities here only.
    def test_snapshots(self):
        self.policy = CombinedPersistencePolicy(
            versioned_entity_event_store=self.version_entity_event_store,
            timestamped_entity_event_store=self.timestamp_entity_event_store,

        )
        event_player = EventPlayer(
            event_store=self.version_entity_event_store,
            mutator=Example.mutate,
            snapshot_strategy=EventSourcedSnapshotStrategy(
                event_store=self.timestamp_entity_event_store
            )
        )

        # Take a snapshot with a non-existent ID.
        self.assertIsNone(event_player.take_snapshot(uuid4()))

        # Create a new entity.
        registered_example = register_new_example(a=123, b=234)

        # Take a snapshot.
        snapshot1 = event_player.take_snapshot(registered_example.id)

        # Replay from this snapshot.
        initial_state = entity_from_snapshot(snapshot1)
        retrieved_example = event_player.replay_entity(registered_example.id,
                                                       initial_state=initial_state,
                                                       gte=initial_state._version)

        # Check the attributes are correct.
        self.assertEqual(retrieved_example.a, 123)

        # Remember the version now.
        version1 = retrieved_example._version

        # Change attribute value.
        retrieved_example.a = 999

        # Remember the version now.
        version2 = retrieved_example._version

        # Change attribute value.
        retrieved_example.a = 9999

        # Remember the version now.
        version3 = retrieved_example._version

        # Check the event sourced entities are correct.
        retrieved_example = event_player.replay_entity(registered_example.id)
        self.assertEqual(retrieved_example.a, 9999)

        # Take another snapshot.
        snapshot2 = event_player.take_snapshot(retrieved_example.id)

        # Check we can replay from this snapshot.
        initial_state = entity_from_snapshot(snapshot2)
        retrieved_example = event_player.replay_entity(
            registered_example.id,
            initial_state=initial_state,
            gte=initial_state._version,
        )
        # Check the attributes are correct.
        self.assertEqual(retrieved_example.a, 9999)

        # Check we can get historical state at version1.
        retrieved_example = event_player.replay_entity(registered_example.id, lt=version1)
        self.assertEqual(retrieved_example.a, 123)

        # Check we can get historical state at version2.
        retrieved_example = event_player.replay_entity(registered_example.id, lt=version2)
        self.assertEqual(retrieved_example.a, 999)

        # Check we can get historical state at version3.
        retrieved_example = event_player.replay_entity(registered_example.id, lt=version3)
        self.assertEqual(retrieved_example.a, 9999)

        # Similarly, check we can get historical state using a snapshot
        initial_state = entity_from_snapshot(snapshot1)
        retrieved_example = event_player.replay_entity(
            registered_example.id,
            initial_state=initial_state,
            gte=initial_state._version,
            lt=version2,
        )
        self.assertEqual(retrieved_example.a, 999)
