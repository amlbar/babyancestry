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
from family.models import IPToken


def fsClient(request):
    try:
        ip = IPToken.objects.get(ip=get_client_ip(request))
        token = ip.access_token
    except IPToken.DoesNotExist:
        token = None
        
    return FamilySearch(settings.USER_AGENT, settings.APP_KEY, 
                        session = token, base=settings.FS_ADDRESS)


def login_user(request):
    # If authenticated, then go back to family tree page
    if request.session.get('logged_in'):
        return HttpResponseRedirect(reverse('family:family_tree'))
    
    # login through familysearch.org
    if request.method == 'POST':
        redirect = request.build_absolute_uri(reverse('accounts:fs_callback')) 
        request.session['logged_in'] = False
        
        fs = fsClient(request)
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
        # get the unique access token of the logged in user
        fs = fsClient(request)
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
        access_token = fs._fs2py(response)['response']['access_token']
        
        # save the user token
        ip = get_client_ip(request)
        try:
            IPToken.objects.get(ip=ip)
        except IPToken.DoesNotExist:
            IPToken.objects.create(ip=ip, access_token=access_token)
        
        # If the user is successfully logged in, set this to True
        request.session['logged_in'] = True

        # print("success logged in")
        return HttpResponseRedirect(reverse('family:family_tree'))
    except:
        # print("not logged in")
        # If the user is not successfully logged in, set this to False
        request.session['logged_in'] = False
        return HttpResponseRedirect(request.GET.get('redirect', '/'))


def logout_user(request):
    try:
        # remove user token
        IPToken.objects.get(ip=get_client_ip(request)).delete()
    except IPToken.DoesNotExist:
        pass
    request.session['logged_in'] = False
    return HttpResponseRedirect(request.GET.get('redirect', '/'))
    
    
def get_client_ip(request):
    # get the ip address
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
