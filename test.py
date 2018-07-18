import os,sys

cmd="""curl 'http://localhost:8000/example/testy/zzz/test?foo=bar' """
print (cmd)
os.system(cmd)
print ("\n")

cmd="""curl 'http://localhost:8000/example/save/test?data=\{"boo":"paw"\}' """
print (cmd)
os.system(cmd)
print ("\n")

cmd="""curl 'http://localhost:8000/example/save/test?data=\[\["boo","paw"\],\[123,"456"\]\]&format=rows' """
print (cmd)
os.system(cmd)
print ("\n")

cmd="""curl -X POST 'http://localhost:8000/example/save/test?format=columns' -d '{"far":["boo","paw"],"zoo":[123,"456"]}' """
print (cmd)
os.system(cmd)
print ("\n")

cmd="""curl -X POST 'http://localhost:8000/example/save/test?format=csv' -d 'f1,f2,f3\n1,22,333\n"four",5,66' """
print (cmd)
os.system(cmd)
print ("\n")

cmd="""curl 'http://localhost:8000/example/search/test?far=paw' """
print (cmd)
os.system(cmd)
print ("\n")
