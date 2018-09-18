import sys, os, json, io, csv
# from django.http import Http404
# from django.shortcuts import get_object_or_404, render
# from django.http import JsonResponse, HttpResponse
# from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
import traceback
import pymongo
from urllib.parse import parse_qs
import djhelpers as dj

hostdir=os.path.dirname(__file__)
hostdir=hostdir[:hostdir.rfind('/')]
base=hostdir
hostdir=hostdir[:hostdir.rfind('/')]
print("hostdir:",hostdir)
sys.path.insert(0, hostdir)

#host=pymongo.MongoClient()
#db=host['test']

static_context = {
    'images': 'static/images/',
    'scripts': 'static/scripts/',
}

modules = {}

def parse_qstring(s):
    q = parse_qs(s)
    for key, val in q.items():
        if type(val)==list and len(val)==1:
            q[key] = val[0]
    return q

@csrf_exempt
def home(request):
#    try:
#        print ("FROM:", request.META['REMOTE_ADDR'], request.META['REMOTE_HOST'], request.body[:150])
#    except:
#        print ("FROM:", request.META['REMOTE_ADDR'], request.META['REMOTE_HOST'], "body was unprintable")

    endpt = request.get_full_path()
    rawquery = ""
    if "?" in endpt:
        rawquery = endpt[endpt.find("?")+1:]
        endpt = endpt[:endpt.find("?")]
    parts = [x for x in endpt.split("/") if x != ""]
    if parts==["favicon.ico"]:
        return dj.html("")
    print ("PARTS:",parts)
    if len(parts)<1:
#        return dj.html('<div>Perhaps you need some help? try <a href="/help/docs">here</a></div>')
        parts=["index", "home"]
    try:
        mod = parts.pop(0)
    except:
        traceback.print_exc()
        return dj.error("must specify a module")
    if mod not in modules:
        print ("Loading", mod)
        try:
#            os.chdir(os.path.dirname(__file__))
#            os.chdir("..")
#            base=os.path.abspath(".")
            os.chdir(base)
            os.chdir("..")
            modules[mod]=__import__(mod)
            os.chdir(base)
            print("Loaded", mod)
        except:
            traceback.print_exc()
            return dj.error("api module not found: %s" % mod)
    try:
        func = parts.pop(0)
    except:
        return dj.error("must specify a function")
    try:
        func = vars(modules[mod])[func]
    except:
        traceback.print_exc()
        return dj.error("api function not found: %s"%endpt)
    print ("ARGS:",parts)
    # print ("POST:",request.POST)
    print ("GET:",request.GET)
    kwords = {}
    format="json"
    data=None
    if '?' in rawquery:
        extra = rawquery[rawquery.find("?"):]
        rawquery = rawquery[:rawquery.find("?")]
        query = parse_qstring(rawquery)
        print("DBG",query)
        if 'url' in query:
            query['url'] += extra
    else:
        query = parse_qstring(rawquery)
    print ("Q:", query)
    for key,val in query.items():
        if key=="data":
            data=bytes(val,encoding='utf8')
        elif key == "format":
            format = val
        else:
            kwords[key]=val
    if request.method=="POST":
        data = request.body#.decode('utf8'))

    if data:
        print ("DATA: %d bytes" % len(data))
        if format=="json":
            data = json.loads(data.decode('utf8'))
        elif format=="rows":
            data = json.loads(data.decode('utf8'))
            j = []
            schema = data.pop(0)
            for row in data:
                j.append(dict(zip(schema,row)))
            data=j
        elif format == "columns":
            data = json.loads(data.decode('utf8'))
            j = []
            m = max([len(x) for x in data.items()])
            for i in range(m):
                row={}
                for k in data.keys():
                    row[k]=data[k][i]
                j.append(row)
            data = j
        elif format == "csv":
            delim = ","
            if 'delimiter' in kwords:
                delim = kwords['delimiter']
                del kwords['delimiter']
            f = io.StringIO(data.decode('utf8'))
            data = []
            r = csv.reader(f, delimiter=delim)
            for schema in r:
                break
            r = csv.reader(f, delimiter=delim)
            n = 0
            for row in r:
                try:
                    x = {}
                    # print( len(schema) , len(row))
                    if len(schema) < len(row):
                        print ("WARNING: unused data in row %d" % n)
                    if len(schema) > len(row):
                        print ("WARNING: unfilled fields in row %d" % n)
                    for key, val in zip(schema, row):
                        x[key] = val
                    data.append(x)
                except:
                    print("ERROR: csv read error at row %d" % n)
                    traceback.print_exc()
                n += 1
            f.close()

        else:
            return dj.error("unknown format: %s" % format)

    if data == None:
        ret = func(*parts, **kwords)
        if "Response" not in str(type(ret)):
            ret = dj.json(ret)
    else:
        if type(data)!=list:
            data=[data]
            count=1
        else:
            count=len(data)
        n=0
        rets=[]
        for row in data:
            try:
                kwords['data']=row
                # print ("CALLFUNC:", parts, kwords)
                ret = func(*parts, **kwords)
                if type(ret)==dict and "error" in ret:
                    ret["rows_processed"]=n
                    return dj.json(ret)
                if count == 1 or ret != None:
                    rets.append(ret)
            except:
                return dj.html(traceback.format_exc())
            n+=1
        if count>1:
            ret=dj.json({"response":rets, "rows_processed": n})
        elif count==1:
            try:
                ret = dj.json(rets[0])
            except:
                ret = "BADJSON: " + str(rets[0])
        else:
            ret = dj.error("No data processed")
    # print ("RETURNS:",ret)
    return ret
