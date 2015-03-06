from django.conf.urls import *

urlpatterns = patterns(
    'family.views',
    url(r'^$', 'family_tree', name='family_tree'),
    url(r'^ancestor/(?P<person_id>[\w\-]+)/$', 'get_ancestor',
        name='get_ancestor'),
    url(r'^descendant/(?P<person_id>[\w\-]+)/$', 'get_descendant',
        name='get_descendant'),
    url(r'^person/(?P<person_id>[\w\-]+)/$', 'get_person_data',
        name='get_person_data'),
)
