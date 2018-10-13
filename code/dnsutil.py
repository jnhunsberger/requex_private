#!/usr/bin/python

import dns.resolver


def test():
    url = "www.google.com"
    #url = "daringfireball.net"
    #url = "gjjvrtvoopgrnxb.co.uk"
    ips = dns.resolver.query(url, "A")

    for ip in ips:
        print(ip)

def lookup_url(url):
    try:
        ips = dns.resolver.query(url, "A")
        print(url, ":", ips[0])
        return ips[0].address
    except:
        print("Failed to find IP for :", url)        
        return 0

def lookup_urls(urls):
    urls_ips_list = []
    for url in urls:
        ip = lookup_url(url)
        if ip != 0:
            urls_ips_list.append((url, ip))
    return urls_ips_list