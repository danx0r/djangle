# djserver
Django recipes FTW

copy example.py to .. level & rename

test:

    > curl 'localhost:8000/example/testx/ass/b/c?fish=ahard+nose&RAWDATA=foursquare'
    ass b c ahard nose and 10 bytes of raw data

using POST:

    > curl -X POST -d 'brazz==~23345' "localhost:8000/example/testx/arse/?arg2=4&ass=smith&fish=5"
    arse 4 smith 5 and 13 bytes of raw data
