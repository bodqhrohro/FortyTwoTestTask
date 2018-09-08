from django.test import TestCase
from django.core.urlresolvers import reverse

import arrow
from time import sleep

REQUEST_DELAY = 0.002


def _get_accesslog_link(timestamp, new_visits):
    milliseconds = int(timestamp.float_timestamp * 1000)
    return '%s?from=%d&new=%d' % (reverse('accesslog'), milliseconds, new_visits)


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
