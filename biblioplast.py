#!/usr/bin/python

# Reads a list of PMID's (one per line) and outputs csv or json
# May need to run: pip install requests xmltodict json unidecode
# json is complete record, csv is not.
# csv columns: PMID, Title, Abstract
# Usage: echo "12345678" | biblioplast.py -j    --or--
# cat ListOfPMIDs.txt | biblioplast.py > pmids_with_title_abs.csv

import argparse
import fileinput
import requests
import xmltodict
import json
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

def setupArgs():
    parser = argparse.ArgumentParser(description='Get PMID record, print CSV/JSON')
    parser.add_argument('-j', '--json',
                        action='store_true',
                        help='Return JSON, default CSV')
    parser.add_argument('--headers',
                        action='store_true',
                        help='[NOT IMPLEMENTED] Print CSV headers' )
    return parser

def getCSV(pmid):
    try:
        r = requests.get('http://www.ncbi.nlm.nih.gov/pubmed/' + pmid + '?report=xml')
        if r.status_code != 200:
            return '{0}, \"Error retriving: {1}\", \"None\"'.format(pmid, r.status_code)
        doc = xmltodict.parse(r.text.replace('&lt;','<').replace('&gt;','>'))['pre']
        title = doc['PubmedArticle']['MedlineCitation']['Article']['ArticleTitle']
        abstract = doc['PubmedArticle']['MedlineCitation']['Article']['Abstract']['AbstractText']
        abstract = abstractIt(abstract)
        return '{0}, \"{1}\", \"{2}\"'.format(pmid, unidecode(title), unidecode(abstract))
    except Exception as error:
        return "{0}, \"Unexpected Error: {1}\", \"None\"".format(pmid, error)

def getJSON(pmid):
    try:
        r = requests.get('http://www.ncbi.nlm.nih.gov/pubmed/' + pmid + '?report=xml')
        doc = xmltodict.parse(r.text.replace('&lt;','<').replace('&gt;','>'))['pre']
        return json.dumps(doc['PubmedArticle']['MedlineCitation'], indent=4)
    except Exception as error:
        return "{pmid: {0}, error: {1}}".format(pmid,error)

def main():
    parser = setupArgs()
    args = parser.parse_args()
    for line in fileinput.input():
        id = line.strip()
        if args.json:
            print(getJSON(id))
            print "\n\n\n\n"
        else:
            print(getCSV(id))


if __name__ == "__main__":
    main()
