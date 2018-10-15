# DNS Background Notes

This file contains my research into the DNS portion of our project solution. There are a lot of

## Top FOSS DNS Servers

- BIND - “Berkeley Internet Name Domain”, because the software originated in the early 1980s at the University of California at Berkeley.
  - the original, maintained by the ISC
  - used by root servers
    -
- NSD/Unbound by NL Net Labs
  - NSD used by root servers
  - unbound is a resolver
    - https://nlnetlabs.nl/projects/unbound/documentation/
    - https://nlnetlabs.nl/documentation/unbound/unbound/
- KnotDNS/KnotResolver
  - used by root servers
  - has a LUA scripting engine
    - https://www.knot-resolver.cz/documentation/
    - https://knot-resolver.readthedocs.io/en/latest/index.html
- PowerDNS
  - has a LUA scripting engine

## DNS Info

BIND documentation
https://www.isc.org/downloads/bind/doc/

DNS for Rocket Scientists
http://zytrax.com/books/dns/


## Kinds of DNS Servers

- Authority
- Resolver

### Authority Server

A DNS Authority Server claims to be the authority for a domain or set of domains. It contains zone files that define SOA, NS, A, MX, TXT, etc. record types.

Ex: berkeley.edu

### Resolver Server

A DNS server that helps clients resolve domains.

How to build and run named with a basic recursive configuration (BIND)
https://kb.isc.org/docs/aa-00768

## DNS Zones

http://zytrax.com/books/dns/ch8/


## DNS Tools

- dig
  - simple lookup of a domain
  - querying with a specific DNS server
  - querying for a specific record type (NS, SOA, TXT, MX)
  - using short command


## ROOT DNS Servers

Root name servers (includes info about the software they run)
https://en.wikipedia.org/wiki/Root_name_server

Map and ownership of root name servers
http://root-servers.org/

Root database:
https://www.iana.org/domains/root/db


## DNS Proxies

Mostly used as load balancers not filters

- NGINX (https://www.nginx.com/blog/load-balancing-dns-traffic-nginx-plus/)
-

## DNS Firewalls

This is a special configuration of a DNS Server that allows you to load Response Policy Zones (RPZ) to take policy action against certain types of requests.

https://dnsrpz.info/

Method 1: Simple, but low updates
1. Create special Zone files in DNS for RPZ
2. Reload zone files into DNS server by restarting server

CON: super slow once zone files get large (RPZs are always large)

Method 2: Hidden Primary
1. Configure architecture such that secondary (slave) servers are only seen by clients. This gives the DNS admin full control over all zones and doesn't need to worry about disrupting traffic
2. Create special RPZ files in primary
3. Reload zone files into Master DNS server by restarting server
4. Perform an incremental zone transfer to slave DNS servers

PRO: better than method 1 as clients are not disrupted with server restarts anytime a zone file is updated

CON: restarting the primary server for every update can still be time consuming

Method 3: DNS Database Integration
1. Store all zones in a database structure
2. Update database with latest RPZ information
3. Configure DNS server to query database for all requests

PRO: lightning speed
CON: requires writing a database device driver in C - only one exists today from RedHat and it is for an LDAP database server.

Method 3: Dynamic DNS
1. Use a DNS server that allows for real-time updates to RPZ
2. Run scripts that regularly update the RPZ with new information as it becomes available

PRO: close to real-time updates
CON: we will likely need to learn LUA

## Info re: Paul Vixie

https://en.wikipedia.org/wiki/Paul_Vixie

- 1994 & 2004 Founded ISC to support the development of BIND
  - He helped the ISC to run the F root name server
  - He helped to run the L root name server
- 1998 Build the first anti-spam service.
- 2013 spun off the security devision of ISC to Farsight Security (see: https://www.isc.org/blogs/isc-spins-off-its-security-business-unit/)
- 2014 Inducted into the Internet Hall of Fame (see: https://www.internethalloffame.org/inductees/paul-vixie)

Current Chairman and CEO of Farsight Security
https://www.farsightsecurity.com/about-farsight-security/team/

Taking Back the DNS
http://www.circleid.com/posts/20100728_taking_back_the_dns/

DNS Firewalls In Action - RPZ vs. Spam
http://www.circleid.com/posts/20120103_dns_firewalls_in_action_rpz_vs_spam/

Found him here responding to a 2017 question about RPZ support in unbound:
https://nlnetlabs.nl/pipermail/unbound-users/2017-April/010122.html

Gave a presentation on at BlackHat 2016 with insights about PassiveDNS
https://www.blackhat.com/asia-16/briefings.html#multivariate-solutions-to-emerging-passive-dns-challenges

## Farsight Security

Offers the DNSDB
https://dnsdb.info/
https://api.dnsdb.info/

Query DNSDB with python
https://github.com/dnsdb/dnsdb-query

## Process JSON at the command line

https://stedolan.github.io/jq/



## DNSTAP
One of the main issues with analyzing DNS is that is requires packet capture and then translation from there into a format useful for processing.

http://dnstap.info/

may be useful for writing DNS requests to a common logging format without packet capture.

## DNS Server & RPZ Support Research

### BIND

RPZs execute not when a query occurs, but after a query response is received.
Supports GeoIP lookups (if compiled with the option)
PRO:
- Excellent documentation
- Has the most robust support of RPZ with multiple triggers and policy responses.

CON:
- Lacks the ability to dynamically update the RPZ without restarting the server
  - Can be configured to read zones from a database, but requires custom drivers to be written.

The latter could be mitigated either:
- through the deployment of more infrastructure

https://jpmens.net/2011/04/26/how-to-configure-your-bind-resolvers-to-lie-using-response-policy-zones-rpz/

### KnotDNS

From cz.nic (Czech Republic)
Runs two root DNS servers

Two tools available:
- KnotDNS
- KnotResolver

Is available in a Docker container:
https://hub.docker.com/r/cznic/knot-resolver/

Can be scripted with LUA

Allows for dynamic policy updates.

Supports GeoIP lookups


### Unbound

PRO:
- Fast
- Has python modules
- RPZ support built by Farsight Security

Paul Vixie would like to meet with us.

### New data sources:

#### Public List of ICANN and many Major Commercial providers valid top-level domains:

Valid top level domains from ICANN and from major commercial providers:
https://publicsuffix.org/list/
https://publicsuffix.org/list/public_suffix_list.dat

### New data sourceTool: ASN info:

Autonomous System Number (used in BGP routing tables)

Governed by the IANA and controlled by the five Regional Internet Registries (RIRs)

This can help us map from IP address to AS number and AS name

Information about their IP to ASN mapping service. Includes downloads from each of the major Registries.
https://www.team-cymru.com/IP-ASN-mapping.html

Web-based whois:
http://whois.cymru.com/cgi-bin/whois.cgi

Python code for querying the IP-ADN mapping tool:
https://pypi.org/project/cymruwhois/#description

Raw data location: ftp://ftp.arin.net/pub/stats/


### DNS Architecture (Proposed):

1. request comes to our DNS server
2. request and response is logged (using DNStap)
3. we read logged requests and enhance with additional info. Additional info includes:
  - ASN, AS Name
  - Additional DNS record types: SOA(?), NS, MX, TXT, CNAME(?). Some of these will be multistage (MX -> MXdomain -> MX IP)
  - IP addresses
  - GeoIP information (IP2Location or MaxMind)
4. Place all the data into our database
5. Analyze the database to determine malicious/non-malicious with our model
6. Update RPZ with all malicious domains

### Database Thoughts

We need a database in which to store this data.

We likely want to keep a historical record over time for things like IP addresses that change. Name Servers that change, etc.


### Docker Info:

https://afourtech.com/guide-docker-commands-examples/



### Interesting:

https://github.com/cbuijs/unbound-dns-firewall/wiki/BIND-RPZ-vs-unbound-dns-firewall


