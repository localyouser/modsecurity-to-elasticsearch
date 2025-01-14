#!/usr/bin/env python
#
# Copyright 2017 Andrea (theMiddle) Menin
# Copyright 2019 localYouser  
# This software is released under the MIT License, see LICENSE.txt
#

import sys, os, getopt, json, time
import codecs
from datetime import datetime,date
from elasticsearch5 import Elasticsearch

# Please, check the elasticsearch URL below:
es = Elasticsearch(['http://localhost:9200'])

# parse arguments
opts, args = getopt.getopt(sys.argv[1:],"hd:",["help","log-directory="])
for i in opts:
	if i[0] == "-d" or i[0] == "--log-directory":
		basedir = i[1]

# set headers name to lowercase
def renameKeys(iterable):
    if type(iterable) is dict:
        for key in iterable.keys():
            iterable[key.lower()] = iterable.pop(key)
            if type(iterable[key.lower()]) is dict or type(iterable[key.lower()]) is list:
                iterable[key.lower()] = renameKeys(iterable[key.lower()])
    elif type(iterable) is list:
        for item in iterable:
            item = renameKeys(item)
    return iterable

# parsing...
def parseLogFile(file):
	# define the index mapping
	settings = {
		"settings": {
			"number_of_shards": 1,
			"number_of_replicas": 0
		},
		"mappings": {
			"modsecurity": {
				"properties": {
					"unixts": {
						"type": "date"
					}
				}
			}
		}
	}

	# set all dict keys to lower
	#d = renameKeys(json.load(open(file,'r','utf-8','ignore')))
	try: 
		fi = open(file,'rb')
		fir = fi.read()
		d = renameKeys(json.loads(fir))
	        # create a unixts field as a timestamp field
        	d['transaction']['unixts'] = int(d['transaction']['unique_id'][0:14].replace('.',''))
        except:
                print "Cannot Analyze or Write Log"
		#print (d)
		print (fir)
	else:
        	# create 1 index per day... you could change it
        	# if you need to store all logs in a single index:
        	index = 'modsecurity_' + str(date.today()).replace('-','')

        	# because objects in array are not well supported,
        	# redefine all "messages" params and values in "msg"
        	new_messages = []
        	new_ruleid = []
        	new_tags = []
        	new_file = []
        	new_linenumber = []
        	new_data = []
        	new_match = []
        	new_severity = []

        	d['transaction']['msg'] = {}

        	for i in d['transaction']['messages']:
                	new_messages.append(i['message'])
                	new_ruleid.append(i['details']['ruleid'])

                	for tag in i['details']['tags']:
                	        if tag not in new_tags:
                	                new_tags.append(tag)

                	new_file.append(i['details']['file'])
                	new_linenumber.append(i['details']['linenumber'])
                	new_data.append(i['details']['data'])
                	new_match.append(i['details']['match'])
                	new_severity.append(i['details']['severity'])

        	d['transaction']['msg']['message'] = new_messages
        	d['transaction']['msg']['ruleid'] = new_ruleid
        	d['transaction']['msg']['tags'] = new_tags
        	d['transaction']['msg']['file'] = new_file
        	d['transaction']['msg']['linenumber'] = new_linenumber
        	d['transaction']['msg']['data'] = new_data
        	d['transaction']['msg']['match'] = new_match
        	d['transaction']['msg']['severity'] = new_severity

        	# remove old messages list
        	del d['transaction']['messages']

        	# if index exists noop, else create it with mapping
        	if es.indices.exists(index):
        	        indexexists=True
        	else:
        	        es.indices.create(index=index, ignore=400, body=settings)

        	# write the log
        	res = es.index(index=index, doc_type="modsecurity", body=d['transaction'])

        	# check if log has been created
        	if res['result'] == 'created':
        	        os.remove(file)
        	        print "Parsed "+str(file)
        	else:
        	        print "Warning: log not created:"
        	        print res

while True:
	for root, subFolders, files in os.walk(basedir):
		for file in files:
			logfile = os.path.join(root, file)
			parseLogFile(file=logfile)

	print "Sleeping for a while..."
	time.sleep(5)

