#!/usr/bin/env python

from madrid_traffic import run
from urllib.parse import urlparse, parse_qs

if __name__ == '__main__':
    import os
    import urllib.parse
    query_string = os.getenv('QUERY_STRING')
    qs = urllib.parse.parse_qs(query_string);
    print("Content-Type: text/html\n")
    try:
        r = run(**{k:v[0] for k, v in qs.items()})
        print ("OK")
    except Exception as e:
        print ("error: %s" % str(e))
