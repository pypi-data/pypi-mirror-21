from eventsourcing.tests.example_application_tests.base import ExampleApplicationTestCase
from eventsourcing.tests.sequenced_item_tests.test_sqlalchemy_active_record_strategy import \
    WithSQLAlchemyActiveRecordStrategies


class TestExampleApplicationWithSQLAlchemy(WithSQLAlchemyActiveRecordStrategies, ExampleApplicationTestCase):
    pass
