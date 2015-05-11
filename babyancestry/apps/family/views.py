from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.conf import settings

from urllib import urlencode
from urllib2 import HTTPError
from urlparse import parse_qs

from accounts.views import fsClient
import json


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
    # print(person_id)

    gender = request.GET.get('gender', '')

    ancestors = fs.get(fs.ancestry(person_id, generations = 5))['response']

    persons = []
    for i, val in enumerate(ancestors['persons']):
        person = ancestors['persons'][i]
        person_gender = (person['display']['gender']).lower()

        # ancestors are composed of both boys and girls.
        # if we want to return only the boys then do query on person_memories only when a person's gender = male
        # for girls, do query on person_memories only when a person's gender = female
        # for both boys and girls, do query on person_memories for each person in ancestors
        if gender == person_gender or gender in ['all', '']:
            persons.append(person)

    # just for reviewing your json output. will be removed in the future
    format = request.GET.get('format', '').lower()
    if format and format == 'json':
        result = json.dumps(persons,indent=4)
        return HttpResponse(result,content_type="json")


    return render(request, 'family/ancestry.html', {
        'ancestry': persons
    })
    
def get_person_data(request, person_id):
    fs = fsClient(request)
    person = fs.get(fs.person(person_id))['response']['persons'][0]
    memories = fs.get(fs.person_memories(person_id))['response']
    if memories:
        person['stories'] = []
        has_image = False
        for src_desc in memories['sourceDescriptions']:
            if src_desc['mediaType'] == 'text/plain':
                person['stories'].append(src_desc)
            elif src_desc['mediaType'] in ['image/jpeg','image/png'] and not has_image:
                person['thumbnail'] = src_desc['links']['image-thumbnail']['href']
                has_image = True
    
    try:
        life_sketch = person['facts'][1]['value']
    except(IndexError, KeyError):
        life_sketch = ''

    format = request.GET.get('format', '').lower()
    if format and format == 'json':
        result = json.dumps(person,indent=4)
        return HttpResponse(result,content_type="json")

    return render(request, 'family/person_info.html', {
        'person': person,
        'life_sketch': life_sketch,
        'fs_address': settings.FS_ADDRESS
    })

def leave_comments(request):
    if not request.session.get('logged_in'):
        return HttpResponseRedirect(reverse('accounts:login'))
        
    return render(request, 'family/comments.html')

