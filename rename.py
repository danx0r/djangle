import os, sys

new = sys.argv[1]

def do(path):
    oldpath = os.path.abspath('.')
    os.chdir(path)
#     print "-->", path
    for f in os.listdir(path):
#         print "---->", f
        if f[:4] == ".git" or f[-4:] == ".pyc" or f == __file__:
            continue
        f = os.path.abspath(f)
        if os.path.isdir(f):
            do(f)
        else:
            print f
            g = open(f)
            s = g.read()
            g.close()
            s = s.replace("djangsimple", new)
            g = open(f, 'w')
#             g.write(s)
            print s
            g.close()
            
    os.chdir(oldpath)
do('.')
