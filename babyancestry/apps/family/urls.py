from django.conf.urls import *

urlpatterns = patterns(
    'family.views',
    url(r'^$', 'family_tree', name='family_tree'),
    url(r'^comments/$', 'leave_comments', name='leave_comments'),
    url(r'^ancestor/(?P<person_id>[\w\-]+)/$', 'get_ancestor', name='get_ancestor'),
    url(r'^person/(?P<person_id>[\w\-]+)/$', 'get_person_data', name='get_person_data'),
)
