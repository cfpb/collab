from django.conf import settings
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from core.models import Person, OrgGroup
from core.utils import json_response


TEMPLATE_PATH = 'stats/'


def _create_params(req):
    p = {'active_app': 'Stats', 'app_link': reverse('stats:dashboard')}
    if settings.WIKI_INSTALLED:
        p['wiki_installed'] = True
        p['wiki_search_autocomplete_json_url'] = \
            settings.WIKI_SEARCH_URL % ('5', '')
    p.update(csrf(req))
    return p


@user_passes_test(lambda u: u.is_superuser)
def dashboard(req):
    p = _create_params(req)
    p['num_active_users'] = get_user_model().objects.filter(is_active=True).count()
    return render_to_response(TEMPLATE_PATH + 'dashboard.html', p,
                              context_instance=RequestContext(req))


@user_passes_test(lambda u: u.is_superuser)
def groups_list(req):
    p = _create_params(req)
    p['groups'] = Group.objects.all()
    return render_to_response(TEMPLATE_PATH + 'groups_list.html', p,
                              context_instance=RequestContext(req))


@user_passes_test(lambda u: u.is_superuser)
def group_users_emails(req, group_name):
    g = get_object_or_404(Group, name=group_name)
    emails = ''
    for u in g.user_set.all():
        emails += u.email + ', '
    return HttpResponse(emails)


@user_passes_test(lambda u: u.is_superuser)
def staff_directory_profile_pics(req):
    active_profiles = Person.objects.filter(user__is_active=True)
    pics_count = 0
    # it does not appear that there is a way to do this through a query
    for p in active_profiles:
        if not p.photo_file.name == 'avatars/default.jpg':
            pics_count += 1
    return HttpResponse(pics_count)


@user_passes_test(lambda u: u.is_superuser)
def users_by_division_json(req):
    result = {}
    divisions = OrgGroup.objects.filter(
        parent=None).exclude(title__icontains="Region").order_by('title')
    for d in divisions:
        result[d.title] = get_user_model().objects.filter(is_active=True).filter(
            Q(person__org_group=d) |
            Q(person__org_group__parent=d)).order_by(
            'last_name', 'first_name').count()
    result_json = []
    for k in result.keys():
        result_json.append({'name': k, 'value': result[k]})
    return json_response(result_json)
