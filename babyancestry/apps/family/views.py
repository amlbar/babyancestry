from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from urllib import urlencode
from urllib2 import HTTPError
from urlparse import parse_qs

from accounts.views import fsClient
import pprint

def family_tree(request):
    # If not authenticated, then go back to login page
    if not request.session.get('logged_in'):
        return HttpResponseRedirect(reverse('accounts:login'))
    
    try:
        fs = fsClient(request)
        person = fs.get(fs.current_user())['response']['users'][0]
        ancestors = fs.get(fs.ancestry(person['personId']))['response']
    except HTTPError:
        # If token is expired, logged out user
        return HttpResponseRedirect(reverse('accounts:logout'))
    
    pp = pprint.PrettyPrinter(indent=4)
    print 'PERSON..'
    pp.pprint(person)
    print 'Ancestry..'
    pp.pprint(ancestors)

    return render(request, 'family/family_tree.html', {
        'ancestors': ancestors,
        'given_name': person['givenName'],
    })
