import unicodedata
from django.core.exceptions import ObjectDoesNotExist


def user_has_profile(user):
    """
        Returns true if the user has a profile, else returns false
    """
    try:
        user.get_profile()
    except ObjectDoesNotExist:
        return False
    return True


def user_form_data(user):
    return {'first_name': user.first_name, 'last_name': user.last_name,
            'email': user.email,
            'mobile_phone': format_phone_number(user.person.mobile_phone),
            'office_location': None if not user.person.office_location else
            user.person.office_location.id,
            'office_phone': format_phone_number(user.person.office_phone),
            'home_phone': format_phone_number(user.person.home_phone),
            'desk_location': user.person.desk_location,
            'org_group': user.person.org_group,
            'title': user.person.title, 'what_i_do': user.person.what_i_do,
            'current_projects': user.person.current_projects,
            'stuff_ive_done': user.person.stuff_ive_done,
            'things_im_good_at': user.person.things_im_good_at,
            'allow_tagging': user.person.allow_tagging,
            'email_notifications': user.person.email_notifications,
            }


def format_phone_number(phone):
    if phone is None or phone.strip() == '':
        return ''
    else:
        """
        return '-'.join((phone[:3], phone[3:6], phone[6:]))
        """
        return '(' + phone[:3] + ') ' + phone[3:6] + '-' + phone[6:]

def normalize(string):
    return unicodedata.normalize('NFKD', string).encode('ascii','ignore').strip()
