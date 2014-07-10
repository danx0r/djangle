import os, sys

new = sys.argv[1]

def do(path):
    for f in os.listdir(path):
        if f[:4] == ".git" or f[-4:] == ".pyc" or f == __file__:
            continue
        f = os.path.abspath(f)
        print f
        if os.path.isdir(f):
            do(f)

do('.')
