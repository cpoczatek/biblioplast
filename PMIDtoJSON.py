#!/usr/bin/python

# Reads a list of PMID's (one per line) and outputs full info as JSON.
# May need to run: pip install requests xmltodict
# Usage: echo "12345678" | PMIDtoJSON.py or
# cat ListOfPMIDs.txt | PMIDtoJSON.py > json.txt

import fileinput
import requests
import xmltodict
import json

for line in fileinput.input():
    id = line.strip()
    r = requests.get('http://www.ncbi.nlm.nih.gov/pubmed/' + id + '?report=xml')
    doc = xmltodict.parse(r.text.replace('&lt;','<').replace('&gt;','>'))['pre']
    print(json.dumps(doc['PubmedArticle']['MedlineCitation'], indent=4))
    print "\n\n##############################################################\n\n"
