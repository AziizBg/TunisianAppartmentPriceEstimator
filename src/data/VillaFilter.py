import json
import math
import re
from text_to_num import alpha2digit
from difflib import SequenceMatcher

with open('../../data/PreProcessed/Treated.json', 'r', encoding="utf-8") as file:
    data = json.load(file)

todel = []
for item in data:
    if 'description' not in item.keys():
        continue
    if 'une villa' in item['description'].lower():
        print("bye")
        todel.append(item)

for item in todel:
    data.remove(item)

with open('../../data/PreProcessed/Treated.json', 'w', encoding="utf-8") as file:
    json.dump(data, file, indent=4, ensure_ascii=False)
