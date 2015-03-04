import webbrowser

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

try:
    # Python 3
    from http import server
    from urllib.parse import(urlencode, parse_qs)
except ImportError:
    # Python 2
    import BaseHTTPServer as server
    from urllib import urlencode
    from urlparse import parse_qs

from familysearch import FamilySearch


def fsClient():
    return FamilySearch(settings.USER_AGENT, 
                        settings.APP_KEY, 
                        base=settings.FS_ADDRESS)


def login_user(request):
    # If authenticated, then go back to family tree page
    if request.session.get('logged_in'):
        return HttpResponseRedirect(reverse('family:family_tree'))
    
    # login through familysearch.org
    if request.method == 'POST':
        redirect = request.build_absolute_uri(reverse('accounts:fs_callback')) 
        request.session['logged_in'] = False
        
        fs = fsClient()
        fslogin = fs.root_collection['response']['collections'][0]['links']\
                ['http://oauth.net/core/2.0/endpoint/authorize']['href']
        fslogin = fs._add_query_params(fslogin, {
            'response_type': 'code',
            'client_id': fs.key,
            'redirect_uri': redirect
        })
        
        return HttpResponseRedirect(fslogin)
        
    return render(request, 'accounts/login.html')
    
    
def fs_callback(request):
    try:
        request.session['access_token'] = request.GET.get('code')
        
        fs = fsClient()
        
        url = fs.root_collection['response']['collections'][0]['links']\
            ['http://oauth.net/core/2.0/endpoint/token']['href']
        credentials = urlencode({'grant_type': 'authorization_code',
                                 'code': request.GET.get('code'),
                                 'client_id': fs.key
                                  })
        credentials = credentials.encode("utf-8")
        response = fs._request(url, credentials,
                                 {"Content-Type": "application/x-www-form-urlencoded",
                                 "Accept": "application/json"}, nojson=True)
        
        request.session['session_id'] = fs._fs2py(response)['response']['access_token']
        
        request.session['logged_in'] = True
        return HttpResponseRedirect(reverse('family:family_tree'))
    except:
        request.session['session_id'] = None
        request.session['logged_in'] = False
        return HttpResponseRedirect(request.GET.get('redirect', '/'))


def logout_user(request):
    request.session['session_id'] = None
    request.session['logged_in'] = False
    return HttpResponseRedirect(request.GET.get('redirect', '/'))
