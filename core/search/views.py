import re
import itertools

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_response_exempt, csrf_exempt
from django.conf import settings
from django.utils.encoding import smart_text

from haystack import connections
from haystack.query import SearchQuerySet

from core.utils import json_response
from core.models import Person
from core.taggit.models import Tag
from core.search.models import SuggestedSearchResult

TEMPLATE_PATH = 'search/'

# The search terms that are passed to Elasticsearch need to be escaped
# to HTML entities because that's how Elastic looks them up. This table
# is used to do that; it's ordered because you need to guarantee that
# ampersands are replaced first in order not to break the string.
html_escape_table = OrderedDict()
html_escape_table['&'] = '&amp;'
html_escape_table["'"] = '&#39;'


def escape(text, table):
    result = text
    for k, v in table.items():
        result = result.replace(k, v)
    return result

def _get_indexes():
    index = connections['default'].get_unified_index()
    if not index._built:
        index.build()

    indexes = [i for i in index.indexes.iteritems() if hasattr(i[1], 'PRIORITY')]
    return indexes


def _create_params(req):
    p = {}
    if settings.WIKI_INSTALLED:
        p['wiki_installed'] = True
        p['wiki_search_autocomplete_json_url'] = \
            settings.WIKI_SEARCH_URL % ('5', '')
    p.update(csrf(req))
    return p


@login_required
def index(req, term=''):
    """
        Displays an empty search page with a search box.
    """
    p = _create_params(req)
    return render_to_response(TEMPLATE_PATH + 'search.html', p,
                              context_instance=RequestContext(req))


@login_required
def search_results_json(req, term='', context_models=''):
    all_results = []
    term = req.GET.get('term', '')
    escaped_term = escape(term, html_escape_table)
    context_models = req.GET.get('model', '').split(',')

    p = {}
    indexes = sorted(_get_indexes(),
                     key=lambda index: 0 if index[0].__name__.lower() in
                     context_models else index[1].PRIORITY)

    for index in indexes:
        results = SearchQuerySet().filter(content=escaped_term).models(index[0])
        results_count = results.count()
        for r in results[:5]:
            all_results.append(_create_category(r.display,
                                                r.index_name,
                                                term,
                                                r.model_name,
                                                r.url,
                                                results_count))

    return json_response(all_results)


def _create_category(label, category, term, search_slug, link, results_len):
    if results_len > 5:
        category = category + " (%s more)" % results_len

    return {'label': label, 'category': category, 'link': link,
            'term': term, 'search_slug': search_slug}


@login_required
@csrf_exempt
def search(req, term='', index=''):
    if term == '':
        if req.method == 'POST':
            term = smart_text(req.POST.get('term', ''))
        else:
            term = smart_text(req.GET.get('term', ''))

    term = term.strip()
    if term == '':
        return HttpResponseRedirect(reverse('search:index'))
    escaped_term = escape(term, html_escape_table)

    suggested_results = SuggestedSearchResult.objects.filter(search_term=term.lower())

    p = {}
    p['term'] = term
    p['suggested_results'] = [res.to_dict() for res in suggested_results]

    if index != '' and index != 'all':
        p['index'] = index
        for i in _get_indexes():
            if i[0].__name__.lower() == index:
                p['results'] = SearchQuerySet().filter(
                    content=escaped_term).models(i[0]).order_by('index_priority', 'index_name')
    else:
        p['results'] = SearchQuerySet().filter(
            content=escaped_term).order_by('index_priority', 'index_name')

    if settings.WIKI_INSTALLED:
        p['wiki_installed'] = True
	escaped_term = "'" + escaped_term
	escaped_term = escaped_term.replace('&amp;', '%26')
        p['wiki_search_json_url'] = settings.WIKI_SEARCH_URL % \
            ('50', escaped_term)
    p['WIKI_URL_BASE'] = settings.WIKI_URL_BASE

    return render_to_response(TEMPLATE_PATH + 'search_results.html', p,
                              context_instance=RequestContext(req))


@login_required
@csrf_exempt
def search_tags_json(req, term='', model=''):
    if req.method == 'POST':
        term = req.POST.get('term', '').strip()
        return HttpResponseRedirect(reverse('search:tags_json',
                                            args=[term, ]))
    elif req.method == 'GET':
        if term.strip() == '':
            term = req.GET.get('term', '').strip()
        q = _get_query(term, ['name', ])
        results = Tag.objects.filter(q)
        if model:
            # join with taggeditem may results in duplicates, requires distinct()
            results = results.filter(taggit_taggeditem_items__content_type__name=model).distinct()
        results = results[:5]
        results_json = []
        for r in results:
            results_json.append({'label': r.name, 'value': r.name})
        if len(results_json) > 0:
            return json_response(results_json)
        else:
            return json_response([{}])


def search_persons_json(req):
    json_resp = []
    term = req.GET.get('term', '').strip()
    if term != '':
        q = _get_query(term, ['user__first_name', 'user__last_name'])
        matching_people = Person.objects.filter(q).filter(
            user__is_active=True).distinct()[:5]
        for person in matching_people:
            name = person.user.first_name + ' ' + person.user.last_name
            json_resp.append({'label': name, 'stub': person.stub,
                              'value': name})
    return json_response(json_resp)


def _normalize_query(query_string,
                     findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                     normspace=re.compile(r'\s{2,}').sub):
    """
        Utility function for searching. Splits the query string in
        individual keywords, getting rid of unnecessary spaces and
        grouping quotes words together.
    """
    return [normspace(' ', (t[0] or t[1]).strip())
            for t in findterms(query_string)]


def _get_query(query_string, search_fields):
    """
        Concatenates terms for the database to perform a case insensitve
        query across specified columns.
    """
    query = None
    terms = _normalize_query(query_string)
    for term in terms:
        or_query = None
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query
