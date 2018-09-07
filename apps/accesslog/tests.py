from django.test import TestCase
from django.core.urlresolvers import reverse

from datetime import datetime


class AccessLogViewTests(TestCase):
    def test_access_log_order(self):
        """Access log should contain entries according to previous requests."""
        link1 = reverse('index')
        link2 = reverse('admin')
        self.client.get(link1)
        self.client.get(link2)

        access_log_response = self.client.get(reverse('accesslog'))
        self.assertQuerysetEqual(
            access_log_response.context['visited_links'], [link1, link2, ])

    def test_access_log_new_requests_count_before(self):
        """All requests after timestamp should be counted."""
        timeprobe = datetime.utcnow()
        self.client.get(reverse('index'))
        self.client.get(reverse('admin'))

        access_log_response = self.client.get(reverse('accesslog', kwargs={
            'from': timeprobe
        }))
        self.assertEqual(access_log_response.context['new_requests_count'], 2)

    def test_access_log_new_requests_count_between(self):
        """Only requests after timestamp should be counted."""
        self.client.get(reverse('index'))
        timeprobe = datetime.utcnow()
        self.client.get(reverse('admin'))

        access_log_response = self.client.get(reverse('accesslog', kwargs={
            'from': timeprobe
        }))
        self.assertEqual(access_log_response.context['new_requests_count'], 1)

    def test_access_log_new_requests_count_after(self):
        """All requests are before timestamp and shoudln't be counted."""
        self.client.get(reverse('index'))
        self.client.get(reverse('admin'))
        timeprobe = datetime.utcnow()

        access_log_response = self.client.get(reverse('accesslog', kwargs={
            'from': timeprobe
        }))
        self.assertEqual(access_log_response.context['new_requests_count'], 0)
