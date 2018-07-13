from django.http import JsonResponse, HttpResponse
import json as JSON

def mongo_set(*args):
    pass

def mongo_query(*args):
    pass

def mongo_save_one_json(collection, data):
    data=JSON.loads(data.decode('utf8'))
    return json("saved '%s' to %s" % (data,collection))

def mongo_save_multi_json(collection, data):
    data=JSON.loads(data.decode('utf8'))
    return json("saved '%s' to %s" % (data,collection))

def error(s):
    return JsonResponse({'error': s})

def json(x):
    print ("DEBUG",x)
    if type(x) not in (dict, list):
        x = {'response': x}
    return JsonResponse(x)

def html(x):
    return HttpResponse(x)
