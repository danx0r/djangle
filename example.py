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
    if "RAWDATA" in kw and type(kw["RAWDATA"])==bytes:
        kw["RAWDATA"] = kw["RAWDATA"].decode('utf8')
    return dj.json({"args": args, "keywords": kw})

def testx(arg1, arg2, ass, fish=None, RAWDATA=None):
    return dj.html("%s %s %s %s and %d bytes of raw data type %s" % (arg1, arg2, ass, fish, len(RAWDATA),type(RAWDATA)))

def saveonej(collection,RAWDATA=None):
    return dj.mongo_save_one_json(collection,RAWDATA)

def savemanyj(collection,RAWDATA=None):
    return dj.mongo_save_multi_json(collection,RAWDATA)

def savecolsj(collection,RAWDATA=None):
    dj.mongo_save_columns_json(collection,RAWDATA)

def savecsv(collection,delim=",",RAWDATA=None):
    dj.mongo_save_csv(collection,RAWDATA,delim)

def getall(collection):
    return dj.mongo_query(collection,{})