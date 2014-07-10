# from django.http import Http404
# from django.shortcuts import get_object_or_404, render
# from django.http import HttpResponse, HttpResponseRedirect
# from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, render_to_response

static_context = {
    'images': 'static/images/',
    'scripts': 'static/scripts/',
}

def home(request):
    context = dict(static_context)
    return render(request, 'djangsimple/templates/index.html', context)
