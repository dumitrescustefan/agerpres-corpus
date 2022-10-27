"""
Will select from each category a sample of texts between date x and y
"""
import json
import os.path
import numpy as np
import datetime

DOMAINS = ['politica', 'social', 'cultura', 'regionale', 'economic-intern', 'justitie', 'educatie-stiinta', 'eveniment', 'sanatate', 'mediu', 'politica-externa', 'romania-in-lume', 'stiintatehnica', 'economic-extern', 'mondorama', 'life', 'planeta']
END_DATE = datetime.datetime.strptime('2021-11-01', "%Y-%m-%d").date()
NUMBER_OF_NEWS_PER_CATEGORY = 1000


# load data
data = {}
for domain in DOMAINS:
    print(f"Loading {domain}...")
    file = f'raw_{domain}.json'
    if os.path.exists(file):
        with open(file, 'r', encoding="utf8") as f:
            data[domain] = json.load(f)
    else:
        print(f"Domain {domain} does not exist!")

# process all news
for domain in DOMAINS:
    if domain not in data:
        continue
    print(f"Domain *** {domain} *** has {len(data[domain])} articles... ")
    keys = [k for k in data[domain]]
    for key in keys:
        try:
            date_str = data[domain][key]['date_time']
            date_str = date_str[:date_str.index(' ')]
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            if date > END_DATE:  # filter out by date
                del data[domain][key]
        except:
            del data[domain][key]
    print(f"\t after time filtering it has {len(data[domain])} articles.")


    # select N values from this domain
    if len(data[domain])<NUMBER_OF_NEWS_PER_CATEGORY:
        print(f"Domain {domain} has only {len(data[domain])} entries, less than N! SKIPPING!!!")
        continue

    choices = [int(x) for x in np.linspace(start=0, stop=len(data[domain])-1, num=NUMBER_OF_NEWS_PER_CATEGORY).tolist()]
    choices = sorted(list(set(choices)))

    print(f"\nSelecting news for {domain}: < {choices[:5]} ... {choices[-5:]} > , total news = {len(choices)}")
    keys = [k for k in data[domain]]
    selected = []
    for ch_int in choices:
        key = keys[ch_int]
        selected.append(data[domain][key])
        selected[-1]["key"] = key

    with open(f"selected_{domain}.json", "w", encoding="utf8") as f:
        json.dump(selected, f, indent=2, ensure_ascii=False)
    print(f"Written selected news for {domain}.")
    print("_"*100)
