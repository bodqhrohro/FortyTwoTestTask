from django.test import TestCase
from django.core.urlresolvers import reverse


class ContactPageViewTests(TestCase):
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
    def test_general_info(self):
        """Check if the general info is read properly."""
        general_info = GeneralInfo.objects.all()
        self.assertIn(general_info, ('Name', 'Bohdan'))
        self.assertIn(general_info, ('Last Name', 'Horbeshko'))
        self.assertIn(general_info, ('Date of birth', '06-10-1995'))
        self.assertIn(general_info, ('Bio', 'Mul\nti\nline'))

    def test_contacts(self):
        """Check if the contacts are read properly."""
        contacts = Contacts.objects.all()
        self.assertIn(contacts, ('Email', 'email'))
        self.assertIn(contacts, ('Jabber', 'JID'))
        self.assertIn(contacts, ('Skype', 'id'))
        self.assertIn(contacts, ('', 'Mul'))
        self.assertIn(contacts, ('', 'ti'))
        self.assertIn(contacts, ('', 'line'))
