#this file gets imported by djangle
import sys
import djhelpers as dj
sys.path.append("..")

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
    if "RAWDATA" in kw:
        kw["RAWDATA"] = kw["RAWDATA"].decode('utf8')
    return dj.json({"args": args, "keywords": kw})

def testx(arg1, arg2, ass, fish=None, RAWDATA=None):
    return dj.html("%s %s %s %s and %d bytes of raw data" % (arg1, arg2, ass, fish, len(RAWDATA)))