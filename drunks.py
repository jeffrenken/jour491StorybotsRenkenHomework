import csv

reader = csv.reader(open("drunks.csv", "rU"), dialect=csv.excel)

reader.next()

for row in reader:
    print row[0], "had", row[1], "drinks.",