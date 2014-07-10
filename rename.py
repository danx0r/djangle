import os, sys

old = "djangsimple"
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
            if os.path.basename(f) == old:
                cmd = "git mv %s %s" % (old, new)
                print cmd
                os.system(cmd)
                
        else:
            print f
            g = open(f)
            s = g.read()
            g.close()
            s = s.replace(old, new)
            g = open(f, 'w')
            g.write(s)
            g.close()
            
    os.chdir(oldpath)
do('.')
print "remember to commit!"