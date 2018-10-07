#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Libraries
import zipfile
import numpy as np
import pandas as pd
import re
import os
import time
import sys

# change current working directory to the data directory
os.chdir('../data/2018-10-06/')

# open ZIP files in cwd and extract all the files and store them to disk
zip_file = zipfile.ZipFile('top-1m.csv.zip', 'r')
zip_file.extractall('./')

# importer for Cisco Umbrella 1m Domains
MB = 1024*1024

start_time = time.time()
df_cisco = pd.read_csv('top-1m.csv', sep=',', skip_blank_lines=True, usecols=[1], names=['domain'], engine='c')
end_time = time.time()
read_time = end_time - start_time

# add columns
df_cisco['malware'] = 'NA'
df_cisco['date'] = np.datetime64('2018-10-06')
df_cisco['dga'] = 0

# analyze
print('Time to import Cisco Umbrella: {:>5.3f}s'.format(read_time))
print('Size of dataset in memory: {:>5.3f}MB'.format(sys.getsizeof(df_cisco)/MB))
print('Top 20 rows:')
print(df_cisco.head(n=20))
print('Summary stats:')
print(df_cisco.describe(include='all'))

# importer for Bambenek Consulting DGA High-Confidence Feed
start_time = time.time()
df_dga = pd.read_csv('dga-feed-high.csv', sep=',', header=16, skip_blank_lines=True, usecols=[0,1,2], names=['domain', 'malware', 'date'], dtype={0:str,1:str}, parse_dates=[2], engine='c')

# modify the malware column
reg = re.compile(r'(^.*? )')
prefix_len = len('Domain used by ')
df_dga['malware'] = df_dga['malware'].str[prefix_len:]
df_dga['malware'] = df_dga['malware'].str.extract(r'(^.*? )', expand=True)
df_dga['malware'] = df_dga['malware'].str.lower()
df_dga['malware'] = df_dga['malware'].str.strip()

# add columns
df_dga['dga'] = 1

end_time = time.time()
read_time = end_time - start_time

print('Time to import Bambeneck DGA Feed: {:>5.3f}s'.format(read_time))
print('Size of dataset in memory: {:>5.3f}MB'.format(sys.getsizeof(df_dga)/MB))
print('Top 20 rows:')
print(df_dga.head(n=20))
print('Summary stats:')
print(df_dga.describe(include='all'))

# Sort malware by number of domains in the dataset
malware_counts = pd.DataFrame(df_dga.groupby('malware')['domain'].nunique())
malware_counts.sort_values(by=['domain'], ascending=False)

# merge both datasets and write to disk
df_merged = df_cisco.append(df_dga, ignore_index=True)

# write merged dataset to a CSV file
df_merged.to_csv(path_or_buf='merged.csv', sep=',', header=True, index=False)

