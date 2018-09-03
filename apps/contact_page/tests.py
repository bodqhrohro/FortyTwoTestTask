from django.test import TestCase
from django.core.urlresolvers import reverse

from apps.contact_page.models import _model_to_tuple, _keyvalue_to_str, \
    GeneralInfo, Contact

from apps.contact_page.views import _is_multiline, _split_contacts, \
    _contacts_to_string, _add_multiline_flag


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

    def test_is_multiline(self):
        """Test multiline string detection."""
        self.assertTrue(_is_multiline('a\nb'))

    def test_is_not_multiline(self):
        """Test against multiline string detection false-positives."""
        self.assertFalse(_is_multiline('a b'))

    def test_split_contacts_both_types(self):
        """One pile of contacts should become two."""
        contacts = [
            ('Email', 'test'),
            ('WTF', 'test2'),
        ]
        split_contacts = _split_contacts(contacts)
        self.assertEqual(split_contacts, (
            [('Email', 'test')], [('WTF', 'test2')]
        ))

    def test_split_contacts_only_known(self):
        """One pile of contacts should become a full one and an empty one."""
        contacts = [
            ('Email', 'test'),
        ]
        split_contacts = _split_contacts(contacts)
        self.assertEqual(split_contacts, (
            [('Email', 'test')], []
        ))

    def test_split_contacts_only_unknown(self):
        """One pile of contacts should become an empty one and a full one."""
        contacts = [
            ('WTF', 'test2'),
        ]
        split_contacts = _split_contacts(contacts)
        self.assertEqual(split_contacts, (
            [], [('WTF', 'test2')]
        ))

    def test_split_contacts_empty(self):
        """Empty pile of contacts should become two empty ones."""
        contacts = []
        split_contacts = _split_contacts(contacts)
        self.assertEqual(split_contacts, ([], []))

    def test_contacts_to_string(self):
        """A list of contacts should be textually represented nice."""
        contacts = [
            ('Email', 'test'),
            ('WTF', 'test2'),
        ]
        s = _contacts_to_string(contacts)
        self.assertEqual(s, 'Email: test\nWTF: test2')

    def test_add_multiline_flag(self):
        """Multilinity of every second string should be properly detected."""
        strings = [
            ('dummy', 'ab'),
            ('dummy2', 'a b'),
            ('dummy3', 'a\nb'),
        ]
        multilines = _add_multiline_flag(strings)
        self.assertEqual(multilines, [
            ('dummy', {
                'value': 'ab',
                'multiline': False,
            }),
            ('dummy2', {
                'value': 'a b',
                'multiline': False,
            }),
            ('dummy3', {
                'value': 'a\nb',
                'multiline': True,
            }),
        ])


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

    def test_model_to_tuple(self):
        """Model with title and value fields should become a binary tuple."""
        general_info = GeneralInfo.objects.create(title='test', value='test2')
        general_info = _model_to_tuple(general_info)
        self.assertEqual(general_info, ('test', 'test2'))

    def test_keyvalue_to_str_with_key(self):
        """Two actual keys should be both shown."""
        general_info = _keyvalue_to_str('test', 'test2')
        self.assertEqual(general_info, 'test: test2')

    def test_keyvalue_to_str_without_key(self):
        """Missing title should not be displayed as well as a colon."""
        general_info = _keyvalue_to_str('', 'test2')
        self.assertEqual(general_info, 'test2')

    def test_keyvalue_to_str_with_null_key(self):
        """None value instead of title shouldn't break the function."""
        general_info = _keyvalue_to_str(None, 'test2')
        self.assertEqual(general_info, 'test2')

    def test_general_info_to_string(self):
        """General info model should be textually represented nice."""
        general_info = GeneralInfo.objects.create(title='test', value='test2')
        general_info = str(general_info)
        self.assertEqual(general_info, 'test: test2')

    def test_contact_to_string(self):
        """Contact model should be textually represented nice."""
        contact = Contact.objects.create(title='test', value='test2')
        contact = str(contact)
        self.assertEqual(contact, 'test: test2')
