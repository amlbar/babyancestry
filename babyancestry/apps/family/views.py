from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from accounts.views import fsClient

@login_required()
def family_tree(request):
    fs = fsClient()
    
    return render(request, 'family/family_tree.html', {
        
    })
