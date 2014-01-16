from dynamicresponse.response import render_to_response, RequestContext
from core.notifications.models import Notification
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


@login_required
def widget(req):
    return render_to_response('notifications/widget.html',
                              {'notifications': Notification.get_unread(
                                  req.user)},
                              context_instance=RequestContext(req))


@login_required
@csrf_exempt
def mark_as_read(req, id):
    notification = Notification.objects.get(pk=id)
    notification.viewed = True
    notification.save()
    return HttpResponse("OK")


@login_required
@csrf_exempt
def mark_all_as_read(req):
    notifications = Notification.objects.filter(target=req.user,
                                                viewed=False)
    for notification in notifications:
        notification.viewed = True
        notification.save()
    return HttpResponse("OK")
