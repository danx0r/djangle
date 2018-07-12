import sys, json
# from django.http import Http404
# from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse, HttpResponse
# from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, render_to_response
from django.views.decorators.csrf import csrf_exempt
import traceback
import pymongo
import djhelpers as dj

sys.path.append("..")

host=pymongo.MongoClient()
db=host['test']

static_context = {
    'images': 'static/images/',
    'scripts': 'static/scripts/',
}

modules = {}

@csrf_exempt
def home(request):
    endpt = request.get_full_path()
    if "?" in endpt:
        endpt = endpt[:endpt.find("?")]
    parts = [x for x in endpt.split("/") if x != ""]
    print ("PARTS:",parts)
    if len(parts)<1:
        return dj.html("Perhaps you need some help?")

    try:
        mod = parts.pop(0)
    except:
        traceback.print_exc()
        return dj.error("must specify a module")
    if mod not in modules:
        print ("Loading", mod)
        try:
            modules[mod]=__import__(mod)
            print("Loaded", mod)
        except:
            traceback.print_exc()
            return dj.error("api module not found: %s" % mod)
    try:
        func = parts.pop(0)
    except:
        return dj.error("must specify a function")
    try:
        func = vars(modules[mod])[func]
    except:
        traceback.print_exc()
        return dj.error("api function not found: %s"%endpt)
    print ("ARGS:",parts)
    print ("POST:",request.POST)
    print ("GET:",request.GET)
    if request.method=="POST":
        kwords = json.loads(request.body.decode('utf8'))
    else:
        kwords = {}
        for key,val in request.GET.items():
            kwords[key]=val
    try:
        ret = func(*parts, **kwords)
    except:
        return dj.html(traceback.format_exc())
    print ("RETURNS:",ret)
    return ret