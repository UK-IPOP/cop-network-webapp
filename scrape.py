import scholar_network
import csv
import time


def load_scholar_names() -> tuple[set[str], set[str]]:
    authors = set()
    ids = set()
    with open("data/IPOP-Scholars.csv", "r", encoding="utf-8-sig") as f:
        csvreader = csv.DictReader(f)
        for row in csvreader:
            authors.add(row.get("Name"))
            ids.add(row.get("ID"))
    with open("data/COPScholars.csv", "r", encoding="utf-8-sig") as f:
        csvreader = csv.DictReader(f)
        for row in csvreader:
            authors.add(row.get("Name"))
            ids.add(row.get("ID"))
    return authors, ids


authors, ids = load_scholar_names()

for author, id_ in zip(authors, ids):
    scholar_network.scrape_single_author(id_, author)
    time.sleep(5)
