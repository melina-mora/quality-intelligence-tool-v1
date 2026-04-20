import csv

def parse(filepath='data/bugs.csv'):
    with open(filepath, mode='r', encoding='UTF-8') as f:
        reader = csv.DictReader(f)
        return [row for row in reader]
