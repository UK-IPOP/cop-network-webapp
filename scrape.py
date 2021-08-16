import scholar_network
import csv
import time
from tqdm import tqdm


def load_scholar_names() -> tuple[list[str], list[str]]:
    authors = list()
    ids = list()
    with open("data/IPOP-Scholars.csv", "r", encoding="utf-8-sig") as f:
        csvreader = csv.DictReader(f)
        for row in csvreader:
            authors.append(row.get("Name"))
            ids.append(row.get("ID"))
    with open("data/COPScholars.csv", "r", encoding="utf-8-sig") as f:
        csvreader = csv.DictReader(f)
        for row in csvreader:
            authors.append(row.get("Name"))
            ids.append(row.get("ID"))
    return authors, ids


authors, ids = load_scholar_names()
info = [{"name": x, "id": y} for x, y in zip(authors, ids)]


failed = list()

for person in tqdm(info):
    try:
        scholar_network.scrape_single_author(
            person.get("id", ""), person.get("name", "")
        )
    except Exception:
        print(f"{person.get('name')} failed")
        failed.append(person)
    time.sleep(5)


for person in tqdm(failed):
    try:
        scholar_network.scrape_single_author(
            person.get("id", ""), person.get("name", "")
        )
    except Exception as e:
        print(e)
        print(f"{person.get('name')} failed AGAIN!!")