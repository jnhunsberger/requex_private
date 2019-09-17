# REQUEX.NET Code Repository

__Summary__: A DNS Firewall service that moves beyond the blacklist to identify previously undiscovered threats.

## Team Cyber
requex.net was developed by the following MIDS students for the UC Berkeley MIDS program w210 Capstone in the Fall 2018 semester.

- Jason Hunsberger
- Aniruddh Nautiyal
- Surya Nimmagadda
- Elizabeth Shulok

## Description
Malware and hacking is an issue that affects all of society. In 2016 alone, cyber attacks cost the US economy over $100B. These attacks not only affect the economy, but the general public as well.

Once a computer is infected, the malware establishes communication with command and control servers which allows malware to download new attack instructions or to monetize their botnet by selling access to the network of infected computers.

Today, malware uses the Domain Name System (or DNS) to hide its command and control servers. It does this by using domain generating algorithms (or DGAs) to flood DNS with requests for thousands of spurious domain names.

Traditionally, security teams use blacklists to block these communications. Unfortunately, blacklists are not effective against domain generating algorithms: there are thousands of domains being generated every day. Defenders cannot keep up with the deluge.

To solve the problems presented by malware that uses domain generation algorithms, our team is building Reque✘ DNS - an intelligent DNS firewall with an integrated deep-learning model that can block requests to algorithm-generated domains. This blockage prevents the malware from communicating with its command and control servers.

## Directories
The directories in this repo contain the following information:

- ./code - all our Python, Docker, Flask, and TensorFlow code
- ./data - details data sources and used by scripts for data processing
- ./dns - our research into DNS architecture and integration
- ./gcp - the data pipeline scripts
- ./papers - research supporting our solution
- ./resources - various images, etc

