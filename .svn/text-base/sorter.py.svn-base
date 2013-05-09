'''
Sorts an optimal file first by the association key column and then the account id
column.

Input:
 data.csv -- Optimal File. Should be in the directory where script is ran from.

Output:
 sorted.csv -- Sorted Optimal File is created in same directory script is ran from.
'''

import csv
import operator

ASSOCIATION_KEY = 2
ACCOUNT_ID = 1

with open('data.csv', 'rb') as f:
    reader = csv.reader(f)
    data = list(reader)
    headers = data.pop(0)

data.sort(key=operator.itemgetter(ASSOCIATION_KEY, ACCOUNT_ID))
  
with open('sorted.csv', 'wb') as f:
    f.write(','.join(headers) + '\n')
    writeit = csv.writer(f)
    writeit.writerows(data)