from collections import namedtuple
from uuid import UUID

from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Float, String

from eventsourcing.application.policies import PersistencePolicy
from eventsourcing.example.domainmodel import register_new_example
from eventsourcing.example.infrastructure import ExampleRepository
from eventsourcing.infrastructure.eventstore import EventStore
from eventsourcing.infrastructure.sequenceditemmapper import SequencedItemMapper
from eventsourcing.infrastructure.sqlalchemy.activerecords import SQLAlchemyActiveRecordStrategy, \
    SqlIntegerSequencedItem
from eventsourcing.infrastructure.sqlalchemy.datastore import Base, SQLAlchemyDatastore, SQLAlchemySettings
from eventsourcing.tests.datastore_tests.base import AbstractDatastoreTestCase

# This tests extending the sequenced item class with some more fields. How easy is it?
# Just needed to define the extended type, define a suitable active record
# class, and extend the sequenced itemevent mapper to derive values for the
# extra attributes. It's easy.

# Define the sequenced item class.
ExtendedSequencedItem = namedtuple('ExtendedSequencedItem',
                                   ['sequence_id', 'position', 'topic', 'data', 'timestamp', 'event_type'])


# Extend the database table definition to support the extra fields.
class SqlExtendedIntegerSequencedItem(SqlIntegerSequencedItem):
    # Timestamp of the event.
    timestamp = Column(Float())

    # Type of the event (class name).
    event_type = Column(String(100))


# Extend the sequenced item mapper to derive the extra values.
class ExtendedSequencedItemMapper(SequencedItemMapper):
    def construct_item_args(self, domain_event):
        args = super(ExtendedSequencedItemMapper, self).construct_item_args(domain_event)
        timestamp = domain_event.timestamp
        event_type = domain_event.__class__.__qualname__
        return args + (timestamp, event_type)


# Define an application object.
class ExampleApplicationWithExtendedSequencedItemType(object):
    def __init__(self, datastore):
        self.event_store = EventStore(
            active_record_strategy=SQLAlchemyActiveRecordStrategy(
                datastore=datastore,
                active_record_class=SqlExtendedIntegerSequencedItem,
                sequenced_item_class=ExtendedSequencedItem,
            ),
            sequenced_item_mapper=ExtendedSequencedItemMapper(
                sequenced_item_class=ExtendedSequencedItem,
                event_sequence_id_attr='entity_id',
                event_position_attr='entity_version',
            )
        )
        self.repository = ExampleRepository(
            event_store=self.event_store,
        )
        self.persistence_policy = PersistencePolicy(self.event_store)

    def close(self):
        self.persistence_policy.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class TestExampleWithExtendedSequencedItemType(AbstractDatastoreTestCase):
    def setUp(self):
        super(TestExampleWithExtendedSequencedItemType, self).setUp()
        self.datastore.setup_connection()
        self.datastore.setup_tables()

    def tearDown(self):
        self.datastore.drop_tables()
        self.datastore.drop_connection()
        super(TestExampleWithExtendedSequencedItemType, self).setUp()

    def construct_datastore(self):
        return SQLAlchemyDatastore(
            base=Base,
            settings=SQLAlchemySettings(),
            tables=(SqlExtendedIntegerSequencedItem,),
        )

    def test(self):
        with ExampleApplicationWithExtendedSequencedItemType(self.datastore) as app:
            # Create entity.
            entity1 = register_new_example(a='a', b='b')
            self.assertIsInstance(entity1.id, UUID)
            self.assertEqual(entity1.a, 'a')
            self.assertEqual(entity1.b, 'b')

            # Check there is a stored event.
            all_records = list(app.event_store.active_record_strategy.filter())
            self.assertEqual(len(all_records), 1)
            active_record = all_records[0]
            self.assertEqual(active_record.sequence_id, entity1.id)
            self.assertEqual(active_record.position, 0)
            self.assertEqual(active_record.event_type, 'Example.Created', active_record.event_type)
            self.assertEqual(active_record.timestamp, entity1.created_on)

            # Read entity from repo.
            retrieved_obj = app.repository[entity1.id]
            self.assertEqual(retrieved_obj.id, entity1.id)
