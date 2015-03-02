import webbrowser

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

try:
    # Python 3
    from http import server
    from urllib.parse import parse_qs
except ImportError:
    # Python 2
    import BaseHTTPServer as server
    from urlparse import parse_qs

from familysearch import FamilySearch


def login_user(request):
    # If authenticated, then go back to family tree page
    if request.user.is_authenticated():
        #return HttpResponseRedirect(reverse('genealogy:family'))
        pass
    
    # login through familysearch.org    
    islogin = request.GET.get('login')
    if islogin:
        #redirect = request.build_absolute_uri(reverse('genealogy:family')
        
        fs = FamilySearch(settings.USER_AGENT, 
                          settings.APP_KEY, 
                          base=settings.FS_ADDRESS)
        # fslogin = fs.root_collection['collections'][0]['links']\
        fslogin = fs.root_collection['response']['collections'][0]['links']\
                ['http://oauth.net/core/2.0/endpoint/authorize']['href']
        fslogin = fs._add_query_params(fslogin, {
           'response_type': 'code',
           'client_id': fs.key,
           'redirect_uri': settings.FS_REDIRECT_URI
        })
        return HttpResponseRedirect(fslogin)
        
    return render(request, 'accounts/login.html', {
        #'data': request.META.get('HTTP_HOST')
    })


def logout_user(request):
    if request.user.is_authenticated():
        fs = FamilySearch(settings.USER_AGENT, 
                          settings.APP_KEY, 
                          base=settings.FS_ADDRESS)
        fs.logout()
    return HttpResponseRedirect(request.GET.get('redirect', '/'))
