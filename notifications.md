---
layout: base
title: Notifications
---

## Notifications

Collab has a built in notifications system. Basically, any app can send a notification to a user. 
The notification will show up in the main navigation for the user to read or hide.

To add notifications within an app you just:


    from core.notifications.models import Notification
    from core.notifications.email import EmailInfo

    email_info = EmailInfo(
      subject=title,
      text_template='path/to/template.txt',
      html_template='path/to/template.html',
      to_address=user.email
    )

    Notification.set_notification(req.user, req.user, "notified", user_form,
                                user_form.owner, title, url, email_info)



### Options


set_notification the following parameters (in order):

* `owner`: the user who is creating the notification.
* `actor`: the user who is being referred on the notification.
* `verb`: of what the user is being notified.
* `obj`: the object to which the notification refers.
* `target`: the user who is notified.
* `title`: the title of the notification.
* `url` (optional): the url for the page to which the notification refers.
* `email_info` (optional): the email_info object referring the email to be sent.