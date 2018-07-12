from django.http import JsonResponse, HttpResponse

def mongo_set(*args):
    pass

def mongo_query(*args):
    pass

def error(s):
    return JsonResponse({'error': s})

def json(x):
    print ("DEBUG",x)
    if type(x) not in (dict, list):
        x = {'response': x}
    return JsonResponse(x)

def html(x):
    return HttpResponse(x)
