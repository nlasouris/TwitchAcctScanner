#! /usr/bin/env python3

# Looks through newaccts.csv (generated by NewAcctScanner.py) to find matches for a specific pattern and outputs a new file with the matching usernames and their corresponding IDs and creation dates.

import csv

def teststr(string1):
  # Edit this to include however complex a pattern match you want
  if string1.lower().find('elon_musk')>=0: # Search for specific substring
    return True
  else:
    return False  

with open('newaccts.csv', 'r', newline='') as acctfile, open('elon_musk-20210821-1200.csv', 'w', newline='') as botfile:
  reader = csv.reader(acctfile)
  for row in reader:
    name = row[0]
    if teststr(name):
      botfile.write('{0},{1},{2}\n'.format(row[0],row[1],row[2]))


