import json
import re

from text_to_num import alpha2digit

with open('data/processed/CleanedProcessed.json', 'r', encoding="utf-8") as file:
    data = json.load(file)

count = 0
for item in data:
    if "floor" not in item.keys() and 'description' in item.keys():
        tempdesc = alpha2digit(item['description'].lower(), "fr").replace('é','').replace("è", "e").replace("é", "e").replace("<strong>","").replace("</strong>","").replace('sixieme',"6").replace("premier", "1").replace("deuxime", "2").replace("troisime", "3").replace("quatrime", "4").replace("etage", "tage").replace("(","").replace(")","").replace("ere","").replace("eme","").replace("em","").replace(":","").replace("me","").replace("er","").replace("er","")
        match = re.search(r"\d+tage|tage\d+", tempdesc.lower().replace(" ",""))
        if match:
            floor = int(match.group().replace("tage",""))
            if floor < 11:
                item["floor"] = floor
                count += 1

# Save the updated data back to the JSON file
with open('data/processed/CleanedProcessed.json', 'w', encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print(f"Updated {count} records with floor information.")
