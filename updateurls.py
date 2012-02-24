#!/usr/bin/env python
import re
import sys
import requests
import fileinput

def was_moved(m, line_no):
    url = m.group(0) 
    response = requests.head(url)
    if response.status_code != 200:
        sys.stderr.write("ERROR - Line %d: %s reponse invalid. Status was %d\n" % (line_no, url,
                response.status_code))
        return url
    response.history.reverse()
    for transaction in response.history:
        if transaction.status_code == 301:
            sys.stderr.write("Line %d: %s -> %s\n" % (line_no, url,
            transaction.headers['location']))
            return transaction.headers['location']
    sys.stderr.write("Line %d: %s still valid\n" % (line_no, url))
    return url

url_re = re.compile("https?://[a-zA-Z0-9%./_-]*")

for number, line in enumerate(fileinput.input()):
    new_line = re.sub(url_re, lambda x: was_moved(x, number), line)
    sys.stdout.write(new_line)




