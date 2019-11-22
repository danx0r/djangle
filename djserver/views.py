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
import endpoints

epdir = dir(endpoints)
funcmap={}
for ep in endpoints.djangle_endpoints:
    funcs = [x for x in epdir if x[:len(ep)+1] == ep+"_"]
    funcmap.update({x[len(ep)+1:]: endpoints.__dict__[x] for x in funcs})

funcnames=funcmap.keys()

print ("funcmap:", funcnames, funcmap)

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
#     os.chdir(hostdir)
    try:
        endpt = request.get_full_path()
        rawquery = ""
        if "?" in endpt:
            rawquery = endpt[endpt.find("?")+1:]
            endpt = endpt[:endpt.find("?")]
        parts = [x for x in endpt.split("/") if x != ""]
        if parts==["favicon.ico"]:
            return dj.html("")
        # print ("PARTS:",parts)
        if len(parts)<1:
    #        return dj.html('<div>Perhaps you need some help? try <a href="/help/docs">here</a></div>')
            parts=["pages", "index"]
        elif len(parts) == 1:
            parts.insert(0, "pages")
        try:
            ep = parts.pop(0)
            if ep not in endpoints.djangle_endpoints:
                return dj.error("Unknown endpoint: %s" % ep)
        except:
            traceback.print_exc()
            return dj.error("must specify a module")
        try:
            func = parts.pop(0)
        except:
            return dj.error("must specify a function")
        if func not in funcnames:
            return dj.error("must specify a valid function")

        func = funcmap[func]
        kwords = {}
        format="json"
        data=None
        query = parse_qstring(rawquery)
        # print ("Q:", query)
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
            # print ("DATA: %d bytes" % len(data))
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
    except:
        status = 500
        trace = traceback.format_exc()
        print ("DJANGLE HTTP ERROR: %d EXCEPTION: %s" % (status, trace.strip().split("\n")[-1]))
        print (trace)
        return dj.error("HTTP 500 error", status=status)