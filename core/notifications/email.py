from django.template import Context
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

from django.conf import settings


class EmailInfo(object):

    def __init__(self, text_template=None, html_template=None,
                 subject=None, to_address=None, from_address=None,
                 context=None):
        self.text_template = text_template
        self.html_template = html_template
        self.subject = subject
        self.to_address = to_address
        self.from_address = from_address
        self.context = context


def email_notification(notification, email_info):
    """
    Adapted from http://stackoverflow.com/questions/2809547/creating-email-templates-with-django

    @param: notifcation
    @type notifcation: L{Notification}

    """

    # require 2 templates and render both?
    plaintext = get_template(email_info.text_template)
    htmly = get_template(email_info.html_template)

    d = Context({'n': notification,
                 'c': email_info.context,
                 'project_url': settings.PROJECT_URL})

    subject, from_email, to = email_info.subject, settings.FROM_ADDRESS, email_info.to_address
    text_content = plaintext.render(d)
    html_content = htmly.render(d)

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to],)
    msg.attach_alternative(html_content, "text/html")

    msg.send()
