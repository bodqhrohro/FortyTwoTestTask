from django.test import TestCase
from django.core.urlresolvers import reverse

from apps.contact_page.models import _model_to_tuple, GeneralInfo, Contact


class ContactPageViewTests(TestCase):
    fixtures = ['contact_page_test_data.json']

    def test_name(self):
        """Simple test for the substring presence."""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Horbeshko")

    def test_general_info(self):
        """Check if the general info is outputted properly."""
        response = self.client.get(reverse('index'))
        self.assertQuerysetEqual(response.context['general_info'], map(repr, [
            ('Name', {
                'value': 'Bohdan',
                'multiline': False,
            }),
            ('Last Name', {
                'value': 'Horbeshko',
                'multiline': False,
            }),
            ('Date of birth', {
                'value': '06-10-1995',
                'multiline': False,
            }),
            ('Bio', {
                'value': 'Mul\nti\nline',
                'multiline': True,
            }),
        ]))

    def test_contacts(self):
        """Check if the contacts are outputted properly."""
        response = self.client.get(reverse('index'))
        self.assertQuerysetEqual(response.context['contacts'], map(repr, [
            ('Email', {
                'value': 'email',
                'multiline': False,
            }),
            ('Jabber', {
                'value': 'JID',
                'multiline': False,
            }),
            ('Skype', {
                'value': 'id',
                'multiline': False,
            }),
        ]))
        self.assertEqual(response.context['other_contacts'], 'Mul\nti\nline')


class GeneralInfoModelTests(TestCase):
    fixtures = ['contact_page_test_data.json']

    def test_general_info(self):
        """Check if the general info is read properly."""
        general_info = map(_model_to_tuple, GeneralInfo.objects.all())
        self.assertIn(('Name', 'Bohdan'), general_info)
        self.assertIn(('Last Name', 'Horbeshko'), general_info)
        self.assertIn(('Date of birth', '06-10-1995'), general_info)
        self.assertIn(('Bio', 'Mul\nti\nline'), general_info)

    def test_contacts(self):
        """Check if the contacts are read properly."""
        contacts = map(_model_to_tuple, Contact.objects.all())
        self.assertIn(('Email', 'email'), contacts)
        self.assertIn(('Jabber', 'JID'), contacts)
        self.assertIn(('Skype', 'id'), contacts)
        self.assertIn(('', 'Mul'), contacts)
        self.assertIn(('', 'ti'), contacts)
        self.assertIn(('', 'line'), contacts)
