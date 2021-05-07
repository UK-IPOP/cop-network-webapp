import scholar_network
import csv
import time


def load_scholar_names() -> tuple[list[str], list[str]]:
    with open("data/IPOP-Scholars.csv", "r", encoding="utf-8-sig") as f:
        csvreader = csv.DictReader(f)
        authors = []
        ids = []
        for row in csvreader:
            authors.append(row.get("Name"))
            ids.append(row.get("ID"))
    return authors, ids


authors, ids = load_scholar_names()

for i, author in enumerate(authors):
    scholar_network.scrape_single_author(ids[i], author)
    time.sleep(5)
