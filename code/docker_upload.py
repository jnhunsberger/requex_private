#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Libraries
import subprocess

subprocess.call(['gcloud', 'docker', '--', 'push', 'gcr.io/w210-capstone-219301/spark-python'])
subprocess.call(['gcloud', 'docker', '--', 'push', 'gcr.io/w210-capstone-219301/mids'])
subprocess.call(['gcloud', 'docker', '--', 'push', 'gcr.io/w210-capstone-219301/kafka'])
subprocess.call(['gcloud', 'docker', '--', 'push', 'gcr.io/w210-capstone-219301/zookeeper'])
