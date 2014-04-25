from django.conf import settings

def collab_context(request):
    return {'collab_context': settings.COLLAB_CONTEXT}
