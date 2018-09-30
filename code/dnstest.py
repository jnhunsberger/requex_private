#!/usr/bin/python

import dns.resolver

url = "www.google.com"
#url = "daringfireball.net"
#url = "gjjvrtvoopgrnxb.co.uk"
ips = dns.resolver.query(url, "A")

for ip in ips:
    print(ip)
