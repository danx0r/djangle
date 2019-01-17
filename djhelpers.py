from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from pymongo import MongoClient
import mongoengine as meng
from django.template import Context
from  django.template import RequestContext
from django.template import Template
import os

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

def error(s):
    print ("ERROR:", s)
    return JsonResponse({'error': s})

def json(x):
    if type(x) not in (dict, list):
        x = {'response': x}
    return JsonResponse(x, safe=False)

def html(x):
    return HttpResponse(x)

def file(fn, context={}):
    print ("DEBUG", os.path.abspath('.'))
    try:
        f = open(fn, encoding="utf8")
        s = f.read()
        f.close()
    except:
        f = open(fn, encoding="latin")
        s = f.read()
        f.close()
    template = Template(s)
    return HttpResponse(template.render(Context(context)))
