from django.test import TestCase
from django.core.urlresolvers import reverse

import arrow
from time import sleep

from .models import AccessLog

REQUEST_DELAY = 0.002


def _arrow_to_timestamp(arrow_timestamp):
    return int(arrow_timestamp.float_timestamp * 1000)


def _get_accesslog_link(arrow_timestamp, new_visits):
    timestamp = _arrow_to_timestamp(arrow_timestamp)
    return '%s?from=%d&new=%d' % (reverse('accesslog'), timestamp, new_visits)


class AccessLogViewTests(TestCase):
    def test_access_log_order(self):
        """Access log should contain entries according to previous requests."""
        link1 = reverse('index')
        link2 = reverse('admin:index')
        self.client.get(link1)
        self.client.get(link2)

        access_log_response = self.client.get(reverse('accesslog'))
        self.assertQuerysetEqual(access_log_response.context['visited_links'],
                                 map(repr, [link1, link2, ]))

    def test_access_log_new_requests_count_before(self):
        """All requests after timestamp should be counted."""
        timeprobe = arrow.utcnow()
        self.client.get(reverse('index'))
        sleep(REQUEST_DELAY)
        self.client.get(reverse('admin:index'))
        sleep(REQUEST_DELAY)

        access_log_response = self.client.get(_get_accesslog_link(timeprobe, 2))
        self.assertEqual(access_log_response.context['new_requests_count'], 2)

    def test_access_log_new_requests_count_between(self):
        """Only requests after timestamp should be counted."""
        self.client.get(reverse('index'))
        sleep(REQUEST_DELAY)
        timeprobe = arrow.utcnow()
        self.client.get(reverse('admin:index'))
        sleep(REQUEST_DELAY)

        access_log_response = self.client.get(_get_accesslog_link(timeprobe, 1))
        self.assertEqual(access_log_response.context['new_requests_count'], 1)

    def test_access_log_new_requests_count_after(self):
        """All requests are before timestamp and shoudln't be counted."""
        self.client.get(reverse('index'))
        sleep(REQUEST_DELAY)
        self.client.get(reverse('admin:index'))
        sleep(REQUEST_DELAY)
        timeprobe = arrow.utcnow()

        access_log_response = self.client.get(_get_accesslog_link(timeprobe, 0))
        self.assertEqual(access_log_response.context['new_requests_count'], 0)


class AccessLogModelTests(TestCase):
    def test_access_log_model_order(self):
        """All stored requests should be retrieved in the same order."""
        AccessLog.objects.create(
            link='test',
            timestamp=_arrow_to_timestamp(arrow.utcnow().shift(seconds=-1)))
        AccessLog.objects.create(
            link='test2',
            timestamp=_arrow_to_timestamp(arrow.utcnow().shift(seconds=-3)))
        AccessLog.objects.create(
            link='test3',
            timestamp=_arrow_to_timestamp(arrow.utcnow().shift(seconds=-2)))

        entries = AccessLog.objects.all()
        entries = [entry.link for entry in entries]
        self.assertEqual(entries, ['test2', 'test3', 'test'])

    def test_access_log_auto_timestamps(self):
        """Automatically generated timestamps should match the present time."""
        entry = AccessLog.objects.create(link='test')

        # the difference shouldn't be more than 5 seconds
        self.assertAlmostEqual(
            _arrow_to_timestamp(arrow.utcnow()),
            entry.timestamp,
            delta=5)

    def test_access_log_duplicated_links(self):
        """Duplicated links should all be stored separately."""
        AccessLog.objects.create(link='test')
        AccessLog.objects.create(link='test')

        entries = AccessLog.objects.all()
        entries = [entry.link for entry in entries]
        self.assertEqual(entries, ['test', 'test'])

    def test_access_log_to_string(self):
        """Accesslog model should be textually represented nice."""
        entry = AccessLog.objects.objects.create(link='test')
        entry = str(entry)
        self.assertEqual(entry, 'test')
