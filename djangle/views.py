import json
# from django.http import Http404
# from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
# from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, render_to_response
import pymongo

host=pymongo.MongoClient()
db=host['test']

static_context = {
    'images': 'static/images/',
    'scripts': 'static/scripts/',
}

def home(request):
    context = dict(static_context)
    context['variable'] = "simple"
    return render(request, 'djangle/templates/index.html', context)

def insert(request):
    # context = dict(static_context)
    # context['variable'] = "compex"
    # return render(request, 'djangle/templates/index.html', context)
    if request.method=="GET":
        s = request.GET.get('insert', None)
    else: #POST
        s=request.body.decode('utf8')
    j=json.loads(s)
    print (j)
    print ("mongo:", db.test.save(j))
    print (j)

    return JsonResponse({"id": str(j['_id'])})