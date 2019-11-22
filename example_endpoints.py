#copy as endpoints.py to folder above:
#cp example_endpoints.py ../endpoints.py
#this file gets imported by djserver
import djhelpers as dj

HOST="mongodb://127.0.0.1:27017"
DB="local"
dj.mongo_set(HOST, DB)

djangle_endpoints=["pages", "example"]
#
# main page
#
def pages_index():
    return dj.html("<html><h1>Djangle All The Way!</h1><a href='/page1'>page 1</a></html>")
#
# another page /page1
#
def pages_page1():
    return dj.html("<html><h1>First things 1st</h1></html>")
#
# /test with template
#
def pages_test():
    return dj.file("test.html", {'x': 'template'})
#
# Create endpoint /version
#
def example_version():
    return dj.json({'version': "0.0.001"})

#
# Create endpoint /api?search=abcdef123
#
# http://localhost/example/testy/arg1?arg2=3
def example_testy(*args, **kw):
    return dj.json({"args": args, "keywords": kw})

def example_testx(arg1, arg2, ass, fish=None, RAWDATA=None):
    return dj.html("%s %s %s %s and %d bytes of raw data type %s" % (arg1, arg2, ass, fish, len(RAWDATA),type(RAWDATA)))

def example_save(collection, data):
    return dj.mongo_save(collection, data)

def example_searchone(collection, **kw):
    print ("RETRIEVE %s KW: %s" % (collection, kw))
    ret = dj.mongo_query_one(collection, kw)
    print ("  RET",ret)
    return dj.json(ret)

def example_search(collection, **kw):
    print ("RETRIEVE %s KW: %s" % (collection, kw))
    ret = dj.mongo_query_many(collection, kw)
    print ("  RET",ret)
    return dj.json(ret)
