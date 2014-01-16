---
layout: base
title: Tagging
---

## Tagging

Collab implements its own version of [taggit](https://github.com/alex/django-taggit).

### Taggit

Taggit is a reusable django app that allows developers to add tagging capabilities to their project.
It provides functionality to tag objects as well as querying them by tag name.

### Customization

All the basic functions are there, but a `tag_category` was added. Tags can be added to multiple objects and you can retrieve them by category.

For example you can have the same tag *"travel"* for both a _Person_ and a _Document_. You can use a *"person"* and a *"document"* `tag_category` to differentiate them.


### How to use it

To add tags you can use the `add_tags` helper:

    from core.taggit.utils import add_tags
    add_tags(person, tag, category_slug, req.user, 'person')