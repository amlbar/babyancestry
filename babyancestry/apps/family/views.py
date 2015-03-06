from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from urllib import urlencode
from urllib2 import HTTPError
from urlparse import parse_qs

from accounts.views import fsClient


def family_tree(request):
    # If not authenticated, then go back to login page
    if not request.session.get('logged_in'):
        return HttpResponseRedirect(reverse('accounts:login'))
    
    try:
        fs = fsClient(request)
        person = fs.get(fs.current_user())['response']['users'][0]
    except HTTPError:
        # If token is expired, logged out user
        return HttpResponseRedirect(reverse('accounts:logout'))

    return render(request, 'family/family_tree.html', {
        'person': person
    })
    

def get_ancestor(request, person_id):
    fs = fsClient(request)
    ancestors = fs.get(fs.ancestry(person_id))['response']
    return render(request, 'family/ancestry.html', {
        'ancestry': ancestors['persons'],
        'gender': request.GET.get('gender')
    })
    
    
def get_descendant(request, person_id):
    fs = fsClient(request)
    descendant = fs.get(fs.descendancy(person_id))['response']
    return render(request, 'family/ancestry.html', {
        'ancestry': descendant['persons'],
        'gender': request.GET.get('gender')
    })
    
    
def get_person_data(request, person_id):
    fs = fsClient(request)
    person = fs.get(fs.person(person_id))['response']['persons'][0]
    #portrait = fs.get('https://sandbox.familysearch.org/platform/tree/persons/KW46-1D7/portrait')
    return render(request, 'family/person_info.html', {
        'person': person
    })
