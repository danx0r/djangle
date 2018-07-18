from django.http import JsonResponse, HttpResponse
from pymongo import MongoClient

def mongo_set(host, db):
    global connection, database
    connection = MongoClient(host)
    database = connection[db]

def mongo_query(*args):
    pass

def mongo_save(collection, data):
    print ("SAVING: %s to %s" % (data, collection))
    return database[collection].insert_one(data)

def error(s):
    print ("ERROR:", s)
    return JsonResponse({'error': s})

def json(x):
    print ("DEBUG",x)
    if type(x) not in (dict, list):
        x = {'response': x}
    return JsonResponse(x)

def html(x):
    return HttpResponse(x)
