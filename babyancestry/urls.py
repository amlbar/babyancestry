from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns(
    "",
    url(r"^admin/", include(admin.site.urls)),
    
    # babyancestry
    url(r'^', include('accounts.urls', namespace="accounts")),
    #url(r'^family/', include('genealogy.urls', namespace='genealogy')),
)

# For serving static files in debug mode
urlpatterns += staticfiles_urlpatterns() + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
