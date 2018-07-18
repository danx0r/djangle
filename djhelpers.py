from django.http import JsonResponse, HttpResponse
from pymongo import MongoClient

def mongo_set(host, db):
    global connection, database
    connection = MongoClient(host)
    database = connection[db]

def mongo_query_one(collection, query):
    ret=database[collection].find_one(query)
    if ret:
        ret=dict(database[collection].find_one(query))
        ret['_id'] = str(ret['_id'])
    return ret

def mongo_query_many(collection, query):
    ret=list(database[collection].find(query))
    for row in ret:
        row['_id'] = str(row['_id'])
    return ret

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
    return JsonResponse(x, safe=False)

def html(x):
    return HttpResponse(x)
