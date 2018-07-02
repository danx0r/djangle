import os, sys

old = bytes(os.path.basename(os.path.abspath('.')), 'utf8')
new = bytes(sys.argv[1], 'utf8')

def do(path):
    oldpath = os.path.abspath('.')
    os.chdir(path)
#     print "-->", path
    for f in os.listdir(path):
#         print "---->", f
        if f[:4] == ".git" or f[-4:] == ".pyc" or f == __file__:
            print ("Skipping rename of", f)
            continue
        f = os.path.abspath(f)
        if os.path.isdir(f):
            print ("recursing into directory", f)
            do(f)
            if os.path.basename(f) == old.decode('utf8'):
                cmd = "git mv %s %s" % (old.decode('utf8'), new.decode('utf8'))
                os.system(cmd)
        else:
            print ("replacing text in file", f)
            g = open(f, 'rb')
            s = g.read()
            g.close()
            s = s.replace(old, new)
            g = open(f, 'wb')
            g.write(s)
            g.close()
            
    os.chdir(oldpath)
do('.')
print ("remember to commit!")
