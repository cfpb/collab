from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from core.helpers import user_has_profile


class CheckForProfile(object):

    def process_request(self, request):
        if not(request.path == reverse('core:register') or
               request.path == reverse('login') or
               'admin' in request.path or
               'widget' in request.path):
            if request.user.is_authenticated():
                if not user_has_profile(request.user) or not request.user.is_active:
                    return HttpResponseRedirect(reverse('core:register'))
