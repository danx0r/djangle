import os
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from pymongo import MongoClient
import mongoengine as meng

def mongo_set(host, db):
    global connection, database
    #pymongo
    connection = MongoClient(host)
    database = connection[db]
    #mongoengine
    meng.connect(db, host=host)

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
    resp = database[collection].insert_one(data)
    if len(str(resp.inserted_id))==24:
        return None
    else:
        return "error saving document"

def mongo_drop_collection(collection):
    database[collection].drop()

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
    return render(None, fn, context)

def auth(kw):
    if 'user' not in kw:
        return error("Must specify a user")
    if 'password' not in kw:
        return error("Must specify a password")
    user = authenticate(username=kw['user'], password=kw['password'])
    print ("AUTHENTIC:", user, user.is_authenticated )
    if user == None:
        return error("Failure to authenticate")
    return True
