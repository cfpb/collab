---
layout: base
title: Widgets
---

## Widgets

Collab uses [django-widgeter](https://github.com/dlapiduz/django-widgeter) to render widgets on the home page and within apps.

## How it works?

Widgeter allows you to create views and templates for blocks of code (widgets).
You can add widgets to your application by adding a `widgets.py` file in the main module.

## Widgets on the Home Page

Collab's home page has two widgeter "blocks": `home` and `home_side`. The first one renders blocks in the main home page feed and the second one on the sidebar.

## Sample widgets.py

Here is a sample `widgets.py` file if you would like to add a widget on the home page sidebar:

    from widgeter.base import Widget

    class HelloWorld(Widget):
        block = 'home_side'
        priority = '1'
        template = 'hello_world/widget.html'

        def get_context(self, context, options=None):
            return { 'message': u'Hello World!' }


For more information please visit: [django-widgeter](https://github.com/dlapiduz/django-widgeter).