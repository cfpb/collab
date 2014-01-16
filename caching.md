---
layout: base
title: Introduction
---

## Improved Caching

Collab uses the [django-cache-tools](https://pypi.python.org/pypi/django-cache-tools/0.1.1) package to improve Django's basic caching.

You can find the full documentation for django cache tools here: [http://django-cache-tools.readthedocs.org/en/latest/](http://django-cache-tools.readthedocs.org/en/latest/)

The basic tools django-cache-tools provides are:

* [Keyable model](http://django-cache-tools.readthedocs.org/en/latest/keyable_model.html)
* [Group Cache](http://django-cache-tools.readthedocs.org/en/latest/group_cache.html)
* [expire_page](http://django-cache-tools.readthedocs.org/en/latest/expire_page.html)


Here are some basic examples:

### Keyable Model

Keyable model lets you cache blocks using a caching key to leverage memcached's LRU algorithm.

First, make a model that inherits from KeyableModel:

    from cache_tools.models import KeyableModel
    # ...
    class Profile(KeyableModel):
    # Your model stuff

Then, pass the cache key to the cache template tag:

    {% raw %}
    {% load cache %}
    {% cache 86400 cache_tools profile.cache_key %}
        <p>
            Lots of very time consuming code.
        </p>
    {% endcache %}
    {% endraw %}



### Group Cache


To cache a page in a group, you just use the cache_page_in_group decorator:

    #views.py
    from cache_tools.tools import cache_page_in_group

    @cache_page_in_group('profiles')
    def show(req, slug):
    # ...

Or, to cache directly in a template:

    # cacheable.html
    {% raw %}
    {% get_group_key group_name as group_key %}

    {% cache 600 page_title group_key %}
    <!-- Long running code -->
    {% endcache %}
    {% endraw %}



To expire the group:

    from cache_tools.tools import expire_cache_group
    # ...
    expire_cache_group('profiles')


### expire_page


If you have a view like:

    #views.py
    @cache_page(60 * 10)
    def show(req, slug):
    # ...

    #urls.py
    # ...
    url(r'^profile/(?P<stub>.*)/$', 'show', name='show_profile'),
    # ...

Then you can use expire_page like:

    from cache_tools.tools import expire_page
    # ...
    expire_page(reverse('show_profile', args=(stub,)))

