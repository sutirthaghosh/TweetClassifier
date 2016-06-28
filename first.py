import csv
import re
l = []
d = {}
s = set()
sum = 0

with open("california_General_Tweet.txt", encoding='utf-8') as tsvfile:
    for line in csv.reader(tsvfile, dialect="excel-tab"):
        line[3]= re.sub('^RT @([a-zA-Z_0-9]*):', '', line[3])
        l.append(line[3])
        if line[3] in d:
            d[line[3]] += 1
        else:
            d[line[3]] = 1
        l = list(set(l))

for key in d.keys():
    print(key, "->", d[key])
    sum = sum + d[key]
print(len(l))
print(sum)
#writer = csv.writer(open('dict.csv', 'w'),dialect="excel-tab")
#for key, value in d.items():
#        writer.writerow([key, value])
