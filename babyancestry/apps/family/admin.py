from django.contrib import admin
from .models import IPToken

class IPTokenAdmin(admin.ModelAdmin):
    pass

admin.site.register(IPToken, IPTokenAdmin)
