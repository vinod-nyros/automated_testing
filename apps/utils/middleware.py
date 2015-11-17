# -*- coding: utf-8 -*-

from django.conf import settings
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect

# from mezzanine

class SSLRedirectMiddleware(object):
    """
    Handles redirections required for SSL when ``SSL_ENABLED`` is ``True``.

    If ``SSL_FORCE_HOST`` is ``True``, and is not the current host,
    redirect to it.

    Also ensure URLs defined by ``SSL_FORCE_URL_PREFIXES`` are redirect
    to HTTPS, and redirect all other URLs to HTTP if on HTTPS.
    """
    def process_request(self, request):
        #settings.use_editable()

        force_host = settings.SSL_FORCE_HOST

        if force_host and request.get_host().split(":")[0] != force_host:
            url = "http://%s%s" % (force_host, request.get_full_path())
            return HttpResponsePermanentRedirect(url)

        if settings.SSL_ENABLED and not settings.DEV_SERVER:
            url = "%s%s" % (request.get_host(), request.get_full_path())

            if request.path.startswith(settings.SSL_FORCE_URL_PREFIXES):
                if not request.is_secure():
                    return HttpResponseRedirect("https://%s" % url)
            elif request.is_secure() and settings.SSL_FORCED_PREFIXES_ONLY:
                return HttpResponseRedirect("http://%s" % url)
