from django.conf.urls import *

urlpatterns = patterns(
    'family.views',
    url(r'^$', 'family_tree', name='family_tree'),
)
