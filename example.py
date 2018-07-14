#this file gets imported by djserver
from djangle import djhelpers as dj

MONGO="mongodb://127.0.0.1:27017"
dj.mongo_set(MONGO, "test_db")

#
# Create endpoint /version
#
def version():
    return dj.json({'version': "0.0.001"})

#
# Create endpoint /api?search=abcdef123
#
def testy(*args, **kw):
    return dj.json({"args": args, "keywords": kw})

def testx(arg1, arg2, ass, fish=None, RAWDATA=None):
    return dj.html("%s %s %s %s and %d bytes of raw data type %s" % (arg1, arg2, ass, fish, len(RAWDATA),type(RAWDATA)))

def save(collection, data):
    return dj.mongo_save(collection, data)
