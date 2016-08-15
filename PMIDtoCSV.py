
# Reads a list of PMID's (one per line) and outputs csv file with
# columns: PMID, Title, Abstract
# May need to run: pip install requests xmltodict unidecode
# Usage: echo "12345678" | PMIDtoCSV.py or
# cat ListOfPMIDs.txt | PMIDtoCSV.py > pmids_with_title_abs.csv

import fileinput
import requests
import xmltodict
from unidecode import unidecode

def abstractIt(abstract):
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
    doc = xmltodict.parse(r.text.replace('&lt;','<').replace('&gt;','>'))['pre']
    #id = doc['PubmedArticle']['MedlineCitation']['PMID']['#text']
    title = doc['PubmedArticle']['MedlineCitation']['Article']['ArticleTitle']
    abstract = doc['PubmedArticle']['MedlineCitation']['Article']['Abstract']['AbstractText']
    abstract = abstractIt(abstract)
    print '{0}, \"{1}\", \"{2}\"'.format(pmid, unidecode(title), unidecode(abstract))
  except Exception as error:
        print "{0}, \"Unexpected Error: {1}\", \"None\"".format(pmid, error)
