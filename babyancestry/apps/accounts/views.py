import webbrowser
import pprint

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


def fsClient():
    return FamilySearch(settings.USER_AGENT, 
                        settings.APP_KEY, 
                        base=settings.FS_ADDRESS)


def login_user(request):
    # If authenticated, then go back to family tree page
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('family:family_tree'))
    
    # login through familysearch.org
    if request.method == 'POST':
        redirect = request.build_absolute_uri(reverse('accounts:fs_callback'))
        fs = fsClient()
        fslogin = fs.root_collection['response']['collections'][0]['links']\
                ['http://oauth.net/core/2.0/endpoint/authorize']['href']
        fslogin = fs._add_query_params(fslogin, {
            'response_type': 'code',
            'client_id': fs.key,
            'redirect_uri': redirect
        })
        return HttpResponseRedirect(fslogin)
        
    return render(request, 'accounts/login.html', {
        'data': request.build_absolute_uri(reverse('accounts:fs_callback'))
    })
    
    
def fs_callback(request):
    try:
        fs = fsClient()
        fs.oauth_code_login(request.GET.get('code'))
        return HttpResponseRedirect(reverse('family:family_tree'))
    except:
        return HttpResponseRedirect(request.GET.get('redirect', '/'))


def logout_user(request):
    if request.user.is_authenticated():
        fs = fsClient()
        fs.logout()
    return HttpResponseRedirect(request.GET.get('redirect', '/'))
