import djangle as dj
import json

MONGO="mongodb://127.0.0.1:27017"

dj.mongo_set(MONGO, "test_db")

def get_version():
    return ("0.0.001")

# def check_upsert(data):
#     j=json.loads(data)
#     k = j.keys()
#     if len(k) != 2:
#         error()
#     if 'data' not in k:
#         error()
#     if 'type' not in k:
#         error()
#     dj.mongo_write(data)
# schema check:
#
# dj.create_endpoint("api",
#                 post=True,
#                 options={'upsert':dj.check_upsert,
#                          'getVersion':get_version,
#                          'search':dj.mongo_read})

dj.create_endpoint("api",
                get=True,
                post=True,
                options={'upsert':dj.mongo_write,
                         'getVersion':get_version})
