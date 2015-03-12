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
        'ancestry': ancestors['persons']
    })
    
    
def get_person_data(request, person_id):
    fs = fsClient(request)
    person = fs.get(fs.person(person_id))['response']['persons'][0]
    memories = fs.get(fs.person_memories(person_id))['response']
    
    if memories:
        memories_links = memories['sourceDescriptions'][0]['links']
        thumbnail = memories_links['image-thumbnail']['href']
    else:
        memories_links = thumbnail = None

    # if person['facts'] and person['facts'][1]:
    try:
        life_sketch = person['facts'][1]['value']
        # else:
    except IndexError:
        life_sketch = '';

    return render(request, 'family/person_info.html', {
        'person': person,
        'image_links': memories_links,
        'thumbnail': thumbnail,
        'memories': memories,
        'life_sketch': life_sketch
    })
