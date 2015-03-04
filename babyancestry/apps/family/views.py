from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from urllib import urlencode
from urlparse import parse_qs

from accounts.views import fsClient

def family_tree(request):
    # If not authenticated, then go back to login page
    if not request.session.get('logged_in'):
        return HttpResponseRedirect(reverse('accounts:login'))
        
    fs = fsClient()
        
    #url = fs.root_collection['response']['collections'][0]['links']\
    #    ['http://oauth.net/core/2.0/endpoint/token']['href']
    #credentials = urlencode({'grant_type': 'authorization_code',
    #                         'code': request.session.get('access_token'),
    #                         'client_id': fs.key
    #                         })
    #credentials = credentials.encode("utf-8")
    #response = fs._request(url, credentials,
    #                         {"Content-Type": "application/x-www-form-urlencoded",
    #                         "Accept": "application/json"}, nojson=True)
    
    return render(request, 'family/family_tree.html', {
        'data': 1
    })
