from django.conf.urls import *

urlpatterns = patterns(
    'accounts.views',
    url(r'^$', 'login_user', name='login'),
    url(r'^fs/callback/$', 'fs_callback', name='fs_callback'),
    url(r'^logout/$', 'logout_user', name='logout'),
)
