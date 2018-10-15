# Libraries
import pandas as pd
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import os
import re

# change current working directory to the data directory
os.chdir('../data')

# Read in dga, skipping the preliminary lines with attribution info
dga_df = pd.read_csv('2018-10-06/dga-feed-high.csv', header=None, skiprows=15)

# Drop the last column
dga_df.drop(dga_df.columns[[3]], axis=1, inplace=True)

# Assign column names
dga_df.columns = ['domain_name', 'malware', 'date']

# modify the malware column
reg = re.compile(r'(^.*? )')
prefix_len = len('Domain used by ')
dga_df['malware'] = dga_df['malware'].str[prefix_len:]
dga_df['malware'] = dga_df['malware'].str.extract(r'(^.*? )', expand=True)
dga_df['malware'] = dga_df['malware'].str.lower()
dga_df['malware'] = dga_df['malware'].str.strip()

# Add column to label these domains malicious
dga_df['dga'] = 1

#calculate total count of dga domains
dga_count = dga_df['domain_name'].count()

# Read in the Cisco Umbrella dataset
cisco_df = pd.read_csv('2018_0923/top-1m.csv', header=None)

# Keep only the second column with the domain names
cisco_df.drop(cisco_df.columns[[0]], axis=1, inplace=True)

# Assign column name
cisco_df.columns = ['domain_name']
# Add column to label these domains as not malicious
cisco_df['dga'] = 0

#calculate total count of non dga domains
cisco_count = cisco_df['domain_name'].count()

#normalize values
cisco_df['name_length'] = cisco_df['domain_name'].str.len()
cisco_df['name_length_normal'] = cisco_df['name_length'].apply(lambda x: x/cisco_count)

dga_df['name_length'] = dga_df['domain_name'].str.len()
dga_df['name_length_normal'] = dga_df['name_length'].apply(lambda x: x/dga_count)

# Combine the two sets
combined = pd.concat([cisco_df, dga_df], ignore_index=True)

# Calculate and chart character frequencies for the dga domain names
dga_counts = Counter(dga_df['domain_name'].str.cat())
df_dga = pd.DataFrame.from_dict(dga_counts, orient='index')
df_dga.columns = ['dga']
print df_dga.sort_index(axis=0,ascending=False)['dga'].plot(kind='barh', color='b', figsize=[12,8])

# Calculate and chart character frequencies for the Cisco domain names
letter_counts = Counter(cisco_df['domain_name'].str.cat())
df_cisco = pd.DataFrame.from_dict(letter_counts, orient='index')
df_cisco.columns = ['cisco']
print df_cisco.sort_index(axis=0,ascending=False)['cisco'].plot(kind='barh', color='b', figsize=[12,8])

df_dga['dga'] = df_dga['dga'].apply(lambda x: x/dga_count)
df_cisco['cisco'] = df_cisco['cisco'].apply(lambda x: x/cisco_count)
# Combine the two sets
combined_count = df_cisco.merge(df_dga, left_index=True, right_index=True)

#chart the letter count between the two sets
fig = combined_count.sort_index(axis=0,ascending=True).plot(kind='bar', color=['skyblue','orange'], figsize=[15,6]).get_figure()
fig.savefig('letter_count.png')

# Add a new column with the length of the domain name
combined['name_length'] = combined['domain_name'].str.len()
combined.hist(column='name_length', bins=50, range=[0, 50], by='dga', layout=[2,1], figsize=[12,6],rwidth=0.8, sharey=True)

# Add a new column with the length of the domain name
combined.hist(column='name_length_normal', bins=40, range=[0, .0001], by='dga', layout=[2,1], figsize=[12,6],rwidth=0.8, sharey=True)

# Add a new column with the heirarchy count for the domain names
# using an intermediate step of breaking up the domain into its subdomains
combined['hierarchy'] = combined['domain_name'].str.split('.')
combined['hierarchy_count'] = [len(c) for c in combined['hierarchy']]

combined.hist(column='hierarchy_count', bins=10, by='malicious', range=[1, 10], layout=[1,2], figsize=[6,4], rwidth=0.8, sharey=True)

# Get the TLD from the hierarchy
combined['tld'] = [c[-1] for c in combined['hierarchy']]

# Chart TLDs
non_dga = combined[(combined['dga'] == 0)]
counts = dict(Counter(non_dga['tld']).most_common(25))

labels, values = zip(*counts.items())

# sort your values in descending order
indSort = np.argsort(values)[::-1]

# rearrange your data
labels = np.array(labels)[indSort]
values = np.array(values)[indSort]

indexes = np.arange(len(labels))

bar_width = 0.35
fig = plt.figure(figsize=(14,6))  # sets the window to 8 x 6 inches

plt.bar(indexes, values)

# add labels
plt.xticks(indexes + bar_width, labels)
plt.show()