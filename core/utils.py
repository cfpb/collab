from django.http import HttpResponse
from django.template.defaultfilters import slugify
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
import json


def json_response(dictionary):
    return HttpResponse(json.dumps(dictionary), mimetype='application/json')
