import csv
import os
import re

with open('instastory.csv', 'r') as f:
    data = csv.DictReader(f)

    for line in data:
        print(line['ï»¿Topic'], line['Part 1'].encode("utf-8", "ignore").decode(), line['Part 2'].encode('utf-8', 'ignore'))
