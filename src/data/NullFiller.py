import json
import math
import re
from text_to_num import alpha2digit
from difflib import SequenceMatcher

with open('../../data/PreProcessed/Treated.json', 'r', encoding="utf-8") as file:
    data = json.load(file)


NulledFields = ["balcony", "parking", "heating", "air_conditioning", "equipped_kitchen", "garage"]
for item in data:
    for field in NulledFields:
        if field not in item.keys():
            item[field] = 'no'

with open('../../data/PreProcessed/Treated.json', 'w', encoding="utf-8") as file:
    json.dump(data, file, indent=4, ensure_ascii=False)
