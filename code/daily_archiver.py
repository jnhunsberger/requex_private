#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''daily_archiver.py - Runs all the archiver scripts sequentially.

'''
import os
import download_external
import extract
import rename
import archive

print("------ Starting daily_archiver....")
download_external.run()
print("------ download_external finished.")
print("------ extract started.")
extract.run()
print("------ extract finished.")
os.chdir('../../../code/')
print("------ rename started.")
rename.run()
print("------ rename finished.")
os.chdir('../../../code/')
print("------ archive started.")
archive.run()
print("------ archive finished.")

print("Daily archiver complete.")
