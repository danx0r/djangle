import os,sys

cmd="""curl 'http://localhost:8000/djtest/save/test?data=\{"boo":"paw"\}' """
print (cmd)
os.system(cmd)
print ("\n")

cmd="""curl 'http://localhost:8000/djtest/save/test?data=\[\["boo","paw"\],\[123,"456"\]\]&format=rows' """
print (cmd)
os.system(cmd)
print ("\n")

cmd="""curl -X POST 'http://localhost:8000/djtest/save/test?format=columns' -d '{"far":["boo","paw"],"zoo":[123,"456"]}' """
print (cmd)
os.system(cmd)
print ("\n")
