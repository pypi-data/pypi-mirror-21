from math import floor
from time import time
from uuid import uuid4

import six

from eventsourcing.domain.model.timebucketedlog import start_new_timebucketedlog
from eventsourcing.example.domainmodel import Example, register_new_example
from eventsourcing.infrastructure.activerecord import AbstractActiveRecordStrategy
from eventsourcing.infrastructure.eventstore import EventStore
from eventsourcing.infrastructure.iterators import SequencedItemIterator
from eventsourcing.infrastructure.timebucketedlog_reader import TimebucketedlogReader, get_timebucketedlog_reader
from eventsourcing.tests.base import notquick
from eventsourcing.tests.core_tests.test_utils import utc_now
from eventsourcing.tests.example_application_tests.base import WithExampleApplication
from eventsourcing.tests.example_application_tests.test_example_application_with_encryption import \
    WithEncryption
from eventsourcing.tests.sequenced_item_tests.test_cassandra_active_record_strategy import \
    WithCassandraActiveRecordStrategies
from eventsourcing.tests.sequenced_item_tests.test_sqlalchemy_active_record_strategy import \
    WithSQLAlchemyActiveRecordStrategies


@notquick()
class PerformanceTestCase(WithExampleApplication):
    def test(self):
        """
        Reports on the performance of Example entity and repo.

        NB: This test doesn't actually assert anything, so it isn't really a test.
        """

        with self.construct_application() as app:

            # Initialise dict of entities.
            self.entities = {}

            report_name = type(self).__name__[4:]
            print("\n\n{} report:\n".format(report_name))

            repetitions = 1  # 10

            # NB: Use range(1, 5) to test whether we can get more than 10000 items from Cassandra.
            for i in six.moves.range(0, 5):
                # Setup a number of entities, with different lengths of event history.
                payload = 3
                # payload = str([uuid4().hex for _ in six.moves.range(100000)])
                example = register_new_example(a=1, b=payload)
                self.entities[i] = example

                # Beat a number of times.
                start_beating = utc_now()
                num_beats = int(floor(10 ** i))
                for _ in six.moves.range(num_beats):
                    example.beat_heart()
                time_beating = utc_now() - start_beating
                print("Time to beat {} times: {:.2f}s ({:.0f} beats/s, {:.6f}s each)"
                      "".format(num_beats, time_beating, num_beats / time_beating, time_beating / num_beats))

                # Get the last n events from the repo.
                def last_n(n):
                    n = min(n, num_beats + 1)
                    assert isinstance(app.example_repo.event_player.event_store, EventStore)
                    ars = app.example_repo.event_player.event_store.active_record_strategy
                    assert isinstance(ars, AbstractActiveRecordStrategy)

                    start_last_n = utc_now()
                    last_n_stored_events = []
                    for _ in six.moves.range(repetitions):
                        iterator = SequencedItemIterator(
                            active_record_strategy=ars,
                            sequence_id=example.id,
                            limit=n,
                            is_ascending=False,
                        )
                        last_n_stored_events = list(iterator)
                    time_last_n = (utc_now() - start_last_n) / repetitions

                    num_retrieved_events = len(last_n_stored_events)
                    events_per_second = num_retrieved_events / time_last_n
                    print(("Time to get last {:>" + str(i + 1) + "} events after {} events: {:.6f}s ({:.0f} events/s)"
                                                                 "").format(n, num_beats + 1, time_last_n,
                                                                            events_per_second))

                for j in range(0, i + 1):
                    last_n(10 ** j)

                # Get the entity by replaying all events (which it must since there isn't a snapshot).
                start_replay = utc_now()
                for _ in six.moves.range(repetitions):
                    example = app.example_repo[example.id]
                    assert isinstance(example, Example)
                    heartbeats = example.count_heartbeats()
                    assert heartbeats == num_beats, (heartbeats, num_beats)

                time_replaying = (utc_now() - start_replay) / repetitions
                print("Time to replay {} beats: {:.2f}s ({:.0f} beats/s, {:.6f}s each)"
                      "".format(num_beats, time_replaying, num_beats / time_replaying, time_replaying / num_beats))

                # Take snapshot, and beat heart a few more times.
                app.example_repo.event_player.take_snapshot(example.id, lte=time())

                extra_beats = 4
                for _ in six.moves.range(extra_beats):
                    example.beat_heart()
                num_beats += extra_beats

                # Get the entity using snapshot and replaying events since the snapshot.
                start_replay = utc_now()
                for _ in six.moves.range(repetitions):
                    example = app.example_repo[example.id]
                time_replaying = (utc_now() - start_replay) / repetitions

                events_per_second = (extra_beats + 1) / time_replaying  # +1 for the snapshot event
                beats_per_second = num_beats / time_replaying
                print("Time to replay snapshot with {} extra beats: {:.6f}s ({:.0f} events/s, {:.0f} beats/s)"
                      "".format(extra_beats, time_replaying, events_per_second, beats_per_second))

                print("")

    def test_log_performance(self):

        with self.construct_application() as app:
            example_id = uuid4()
            log = start_new_timebucketedlog(example_id, bucket_size='year')
            log_reader = get_timebucketedlog_reader(log, app.timestamp_entity_event_store)

            # Write a load of messages.
            start_write = utc_now()
            number_of_messages = 111
            events = []
            for i in range(number_of_messages):
                event = log.append_message('Logger message number {}'.format(i))
                events.append(event)
            time_to_write = (utc_now() - start_write)
            print("Time to log {} messages: {:.2f}s ({:.0f} messages/s, {:.6f}s each)"
                  "".format(number_of_messages, time_to_write, number_of_messages / time_to_write,
                            time_to_write / number_of_messages))

            # Read pages of messages in descending order.
            # - get a limited number until a time, then use the earliest in that list as the position
            position = events[-1].timestamp

            page_size = 10

            # Page back through the log in reverse chronological order.
            previous_position = None
            next_position = None
            count_pages = 0
            total_time_to_read = 0
            total_num_reads = 0
            while True:
                start_read = utc_now()
                page_of_events, next_position = self.get_message_logged_events_and_next_position(log_reader, position,
                                                                                                 page_size)
                time_to_read = (utc_now() - start_read)
                total_time_to_read += time_to_read
                total_num_reads += 1
                count_pages += 1
                if next_position is None:
                    break
                else:
                    previous_position, position = position, next_position

            # Check we got to the end of the line.
            self.assertEqual(count_pages, 11)
            self.assertIsNone(next_position)
            self.assertTrue(previous_position)

            # Page forward through the log in chronological order.
            count_pages = 0
            position = None
            while True:
                start_read = utc_now()
                page_of_events, next_position = self.get_message_logged_events_and_next_position(log_reader, position,
                                                                                                 page_size,
                                                                                                 is_ascending=True)
                time_to_read = (utc_now() - start_read)
                total_time_to_read += time_to_read
                total_num_reads += 1
                count_pages += 1
                if next_position is None:
                    break
                else:
                    position = next_position

            self.assertEqual(count_pages, 11)
            self.assertIsNone(next_position)
            self.assertTrue(previous_position)

            reads_per_second = total_num_reads / total_time_to_read
            messages_per_second = reads_per_second * number_of_messages
            print("Time to read {} pages of logged messages: {:.6f}s ({:.0f} pages/s, {:.0f} messages/s))"
                  "".format(total_num_reads, total_time_to_read, reads_per_second, messages_per_second))

    def get_message_logged_events_and_next_position(self, log_reader, position, page_size, is_ascending=False):
        assert isinstance(log_reader, TimebucketedlogReader), type(log_reader)
        assert isinstance(page_size, six.integer_types), type(page_size)
        assert isinstance(is_ascending, bool)
        if is_ascending:
            gt = position
            lt = None
        else:
            lt = position
            gt = None

        events = log_reader.get_events(gt=gt, lt=lt, limit=page_size + 1, is_ascending=is_ascending)
        events = list(events)
        if len(events) == page_size + 1:
            next_position = events.pop().timestamp
        else:
            next_position = None
        return events, next_position


@notquick()
class TestCassandraPerformance(WithCassandraActiveRecordStrategies, PerformanceTestCase):
    pass


@notquick()
class TestEncryptionPerformance(WithEncryption, TestCassandraPerformance):
    pass


@notquick()
class TestSQLAlchemyPerformance(WithSQLAlchemyActiveRecordStrategies, PerformanceTestCase):
    pass
