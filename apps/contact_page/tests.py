from django.test import TestCase
from django.urls import reverse


class ContactPageTests(TestCase):
    def test_name(self):
        response = self.client.get(reverse('contact_page:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Horbeshko")

    def test_general_info(self):
        response = self.client.get(reverse('contact_page:index'))
        self.assertQuerysetEqual(response.context['general_info'], [
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
        ])

    def test_contacts(self):
        response = self.client.get(reverse('contact_page:index'))
        self.assertQuerysetEqual(response.context['contacts'], [
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
        ])
        self.assertQuerysetEqual(response.context['other_contacts'],
                                 'Mul\nti\nline')
