import os,sys

cmd="""curl 'http://localhost:8000/djtest/saveonej/test?RAWDATA=\{"boo":"paw"\}' """
os.system(cmd)

os.system("echo")

cmd="""curl 'http://localhost:8000/djtest/savemanyj/test?RAWDATA=\[\{"boo":"paw"\},\{"foo":"baw"\}\]' """
os.system(cmd)

