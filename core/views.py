from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect

from core.models import Person, OrgGroup, OfficeLocation, \
    Alert
from core.helpers import user_has_profile, user_form_data
from core.forms import AccountForm, RegistrationForm
from core.notifications.models import Notification
from dynamicresponse.response import render_to_response, RequestContext

import re
import json


TEMPLATE_PATH = 'core/'


def create_params(req):
    p = {}
    if settings.WIKI_INSTALLED:
        p['wiki_installed'] = True
        p['wiki_search_autocomplete_json_url'] = \
            settings.WIKI_SEARCH_URL % ('5', '')
    p.update(req)
    return p


def catch_all(req, pattern):
    pattern = pattern.rstrip('/')
    url = "%s%s" % (settings.APACHE_HOST, pattern)
    return HttpResponseRedirect(url)


def update_user(req):
    try:
        profile = req.user.get_profile()
        org_group = OrgGroup.objects.get(pk=int(req.POST['org_group']))

        if req.POST['office_location'] == "":
            office_location = None
        else:
            office_location = OfficeLocation.objects.get(
                pk=req.POST['office_location'])

        req.user.first_name = req.POST['first_name']
        req.user.last_name = req.POST['last_name']
        req.user.email = req.POST['email']
        mPhone = req.POST['mobile_phone']
        oPhone = req.POST['office_phone']
        hPhone = req.POST['home_phone']
        if mPhone != "":
            mPhone = re.sub(r'\D', "", mPhone)
        if oPhone != "":
            oPhone = re.sub(r'\D', "", oPhone)
        if hPhone != "":
            hPhone = re.sub(r'\D', "", hPhone)
        profile.mobile_phone = mPhone   # req.POST['mobile_phone']
        profile.office_phone = oPhone   # req.POST['office_phone']
        profile.home_phone = hPhone     # req.POST['home_phone']
        profile.org_group = org_group
        profile.office_location = office_location
        profile.desk_location = req.POST['desk_location']
        profile.title = req.POST['title']
        profile.what_i_do = req.POST['what_i_do']
        profile.current_projects = req.POST['current_projects']
        profile.things_im_good_at = req.POST['things_im_good_at']
        profile.allow_tagging = ('allow_tagging' in req.POST)
        profile.email_notifications = ('email_notifications' in req.POST)
        if req.FILES:
            profile.photo_file = req.FILES['photo_file']
        profile.save()
        req.user.save()
        return req.user

    except Exception as e:
        return req.user


def get_front_page_data(user, p):
    p['is_front'] = True
    p['current_user'] = user
    alert = Alert.objects.filter(is_active=True). \
        order_by('-create_date')[:1]
    if len(alert) > 0:
        p['alert'] = alert[0]
    return p


def add_user(req):
    user = req.user
    stub = user.username.split('@')[0]
    user.email = req.POST['email']
    user.first_name = req.POST['first_name']
    user.last_name = req.POST['last_name']
    user.save()
    org_group = OrgGroup(pk=req.POST['org_group'])
    office_location = OfficeLocation(pk=req.POST['office_location'])

    attributes = {
        'user': user,
        'stub': stub,
        'title': req.POST['title'],
        'office_location': office_location,
        'org_group': org_group,
        'office_phone': req.POST['office_phone'],
        'mobile_phone': req.POST['mobile_phone'],
        'home_phone': req.POST['home_phone']
    }

    if req.FILES:
        attributes['photo_file'] = req.FILES['photo_file']

    person = Person(**attributes)
    person.save()
    return user


@login_required
def main(req):
    if not user_has_profile(req.user):
        return HttpResponseRedirect(reverse('core:register'))
    p = create_params(req)
    p = get_front_page_data(req.user, p)
    # p['due_tasks'] = Requirement.due_for_user(req.user)
    # p['pneding_tasks'] = Requirement.pending_for_user(req.user)

    return render_to_response(TEMPLATE_PATH + 'index.html', p,
                              context_instance=RequestContext(req))


@login_required
def apps(req):
    return HttpResponse('')


def register(req):
    office_locations = OfficeLocation.objects.all()
    if req.method == 'POST':
        form = RegistrationForm(req.POST)
        if form.is_valid():
            u = add_user(req)
            return HttpResponseRedirect(reverse('core:landing_page'))
        else:
            return render_to_response('core/register.html',
                                      {'form': form,
                                       'office_locations': office_locations,
                                       'is_registration': True},
                                      context_instance=RequestContext(req))
    else:
        form = RegistrationForm()
        return render_to_response('core/register.html',
                                  {'form': form,
                                   'office_locations': office_locations,
                                   'is_registration': True},
                                  context_instance=RequestContext(req))


@login_required
def user_widget(req):
    return render_to_response(TEMPLATE_PATH + 'user_widget.html', {},
                              context_instance=RequestContext(req))

@login_required
def user_info(req):
    user = {}
    user_info = {}
    user['first_name'] = req.user.first_name
    user['last_name'] = req.user.last_name
    user['stub'] = req.user.get_profile().stub
    user_info['user'] = user

    notifications = Notification.get_unread(req.user)
    fields = ['id', 'title', 'timestamp', 'url']
    tmp_notification = []
    for notification in notifications:
        notification_dict = {}
        for field in fields:
            notification_dict[field] = unicode(getattr(notification, field)).encode("utf-8", "replace")

        tmp_notification.append(notification_dict)

    user_info['notifications'] = tmp_notification

    return HttpResponse(json.dumps(user_info), content_type="application/json")


@login_required
def account(req):
    p = create_params(req)
    departments = OrgGroup.objects.filter(parent=None)
    if req.method == "POST":
        form = AccountForm(req.user, req.POST)
        if form.is_valid():
            u = update_user(req)
            return HttpResponseRedirect('/staff/person/%s/'
                                        % u.get_profile().stub)
        else:
            p['form'] = form
            p['u'] = req.user
            p['depts'] = departments
            return render_to_response('core/profile_settings.html', p,
                                      context_instance=RequestContext(req))
    else:
        u = req.user
        form_data = user_form_data(u)
        form = AccountForm(req.user, form_data)

    p['form'] = form
    p['u'] = req.user
    p['depts'] = departments
    return render_to_response('core/profile_settings.html', p,
                              context_instance=RequestContext(req))
