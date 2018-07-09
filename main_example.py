#this file gets imported by djangle
import djhelpers as dj

MONGO="mongodb://127.0.0.1:27017"
dj.mongo_set(MONGO, "test_db")

#
# Create endpoint /version
#
def version():
    return ("0.0.001")

#
# Create endpoint /api?search=abcdef123
#
def api(search):
    return dj.mongo_query(search)