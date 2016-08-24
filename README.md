# biblioplast
Utility scripts to pull PubMed info as CSV or JSON

Both scrips read PMIDs from stdin (1 per line) and query Pubmed. Currently the JSON output is the full record, while the CSV output is: `PMID, Title, Abstract`

Useful bash:

Get PMID column: `awk -F"," '{print $1}' file.csv`
Check errors: `cat output.csv | grep "Error" | awk -F"," '{print $1}' | python PMIDtoJSON.py | less`
