
# Reads a list of PMID's (one per line) and outputs csv file with
# columns: PMID, Title, Abstract
# May need to run: pip install requests xmltodict unidecode
# Usage: echo "12345678" | PMIDtoCSV.py or
# cat ListOfPMIDs.txt | PMIDtoCSV.py > pmids_with_title_abs.csv

import sys
import fileinput
import requests
import xmltodict
from unidecode import unidecode

def findTitle(doc):
    try:
        if 'ArticleTitle' in doc['PubmedArticle']['MedlineCitation']['Article']:
            return doc['PubmedArticle']['MedlineCitation']['Article']['ArticleTitle']
    except KeyError:
        return 'Error: no key'
    return 'None'

def findAbs(doc):
    try:
        if 'AbstractText' in doc['PubmedArticle']['MedlineCitation']['Article']['Abstract']:
            return doc['PubmedArticle']['MedlineCitation']['Article']['Abstract']['AbstractText']
    except KeyError:
        'Error: no key'
    return 'None'

def abstractIt(abstract):
    if abstract == None:
        return 'None'
    if isinstance(abstract, str) or isinstance(abstract, unicode):
        return abstract
    if isinstance(abstract, list):
        parsed = ''
        for item in abstract:
            parsed += abstractIt(item)
        return parsed
    if isinstance(abstract, dict):
        parsed = ''
        parsed += abstract['@Label'] + ": "
        parsed += abstract['#text'] + " "
        return parsed
    else:
        return 'None'

for line in fileinput.input():
  pmid = line.strip()
  try:
    r = requests.get('http://www.ncbi.nlm.nih.gov/pubmed/' + pmid + '?report=xml')
    if r.status_code != 200:
        print '{0}, \"Error retriving: {1}\", \"None\"'.format(pmid, r.status_code)
        continue
    doc = xmltodict.parse(r.text.replace('&lt;','<').replace('&gt;','>'))['pre']
    title = findTitle(doc)
    abstract = findAbs(doc)
    abstract = abstractIt(abstract)
    print '{0}, \"{1}\", \"{2}\"'.format(pmid, unidecode(title), unidecode(abstract))
    sys.stdout.flush()
  except Exception as error:
        print "{0}, \"Unexpected Error: {1}\", \"None\"".format(pmid, error)
