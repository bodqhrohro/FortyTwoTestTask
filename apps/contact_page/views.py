from django.shortcuts import render


KNOWN_CONTACT_TYPES = ['Email', 'Jabber', 'Skype']


def _is_multiline(str):
    return '\n' in str


def _split_contacts(contacts):
    known_contacts = []
    other_contacts = []
    for type, id in contacts:
        if type in KNOWN_CONTACT_TYPES:
            known_contacts.append((type, id))
        else:
            other_contacts.append((type, id))
    return (known_contacts, other_contacts)


def _contacts_to_string(contacts):
    return '\n'.join([
        (type + ': ' if type else '') + id for type, id in contacts
    ])


def _add_multiline_flag(tuples_list):
    return [(key, {
        'value': entry,
        'multiline': _is_multiline(entry),
    }) for key, entry in tuples_list]


def contact_page(request):
    general_info = [
        ('Name', 'Bohdan'),
        ('Last Name', 'Horbeshko'),
        ('Date of birth', '06-10-1995'),
        ('Bio', 'Mul\nti\nline'),
    ]

    contacts = [
        ('Email', 'email'),
        ('Jabber', 'JID'),
        ('Skype', 'id'),
        ('', 'Mul'),
        ('', 'ti'),
        ('', 'line'),
    ]

    general_info = _add_multiline_flag(general_info)

    known_contacts, other_contacts = _split_contacts(contacts)
    known_contacts = _add_multiline_flag(known_contacts)
    other_contacts = _contacts_to_string(other_contacts)

    return render(request, 'contact_page/contact_page.html', {
        "general_info": general_info,
        "contacts": known_contacts,
        "other_contacts": other_contacts,
    })
