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

    gender = ''
    if 'gender' in request.GET:
        gender = request.GET.get('gender')

    ancestors = fs.get(fs.ancestry(person_id))['response']

    persons = [];
    for i, val in enumerate(ancestors['persons']):
        person = ancestors['persons'][i]
        person_gender = (person['display']['gender']).lower()
        get_thumbnail = False
        if gender == person_gender or gender in ['all', '']:
            person_memories = fs.get(fs.person_memories(person['id']))['response']
            thumbnail = None
            if person_memories:
                thumbnail = person_memories['sourceDescriptions'][0]['links']['image-thumbnail']['href']
            person['thumbnail'] = thumbnail
            persons.append(person)

    return render(request, 'family/ancestry.html', {
        'ancestry': persons
    })
    
def get_person_data(request, person_id):
    fs = fsClient(request)
    person = fs.get(fs.person(person_id))['response']['persons'][0]
    memories = fs.get(fs.person_memories(person_id))['response']
    
    memories_links = thumbnail = None
    if memories:
        memories_links = memories['sourceDescriptions'][0]['links']
        thumbnail = memories_links['image-thumbnail']['href']

    try:
        life_sketch = person['facts'][1]['value']
    except IndexError:
        life_sketch = '';

    return render(request, 'family/person_info.html', {
        'person': person,
        'image_links': memories_links,
        'thumbnail': thumbnail,
        'memories': memories,
        'life_sketch': life_sketch
    })
