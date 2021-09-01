from django.contrib.sites.models import Site


def get_external_url(request, rel_url: str):
    port = request.META['SERVER_PORT']
    if port:
        port = ':' + port

    external_url = ''.join(['http://', Site.objects.get_current().domain, port, rel_url])
    return external_url