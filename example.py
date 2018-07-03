import djangle as dj
import json

MONGO="mongodb://127.0.0.1:27017"

dj.set_mongo(MONGO, "test_db")

def get_version():
    return ("0.0.001")

def check_upsert(data):
    j=json.loads(data)
    k = j.keys()
    if len(k) != 2:
        error()
    if 'data' not in k:
        error()
    if 'type' not in k:
        error()
    dj.write_mongo(data)

# simple:

dj.create_endpt("api",
                get=True,
                post=True,
                options={'upsert':dj.write_mongo,
                         'getVersion':get_version})
# schema check:

dj.create_endpt("api",
                post=True,
                options={'upsert':dj.check_upsert,
                         'getVersion':get_version})
