import traceback
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.conf import settings
from pymongo import MongoClient
import mongoengine as meng
import mimetypes

def mongo_set(host, db):
    global connection, database
    #pymongo
    connection = MongoClient(host)
    database = connection[db]
    #mongoengine
    meng.connect(db, host=host)
    return database

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
    # print ("SAVING: %s to %s" % (data, collection))
    return database[collection].insert_one(data)

def error(s, status=200):
    if status == 200:
        return JsonResponse({'error': s})
    if settings.DEBUG:
        print("STATUS: %d ERROR: %s" % (status, s))
        s += "\n" + traceback.format_exc()
    return HttpResponse(s, content_type='text/plain', status = status)

def json(x):
    if type(x) not in (dict, list):
        x = {'response': x}
    return JsonResponse(x, safe=False)

def html(x):
    return HttpResponse(x)

def file(fn, context={}):
    return render(None, fn, context)

def binary(fn, typ):
    f=open(fn, 'rb')
    dat=f.read()
    f.close()
    ret=HttpResponse(dat, content_type=mimetypes.guess_type(fn))
    return ret