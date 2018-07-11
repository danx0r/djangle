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
    return dj.html("args: %s keywords: %s" % (args,kw))