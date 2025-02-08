import json

with open('../../data/processed/processed.json', 'r', encoding="utf-8") as file:
    data = json.load(file)


count = 0
for item in data:
    if 'description' in item.keys():
        if 'garage' in item['description'].lower():
            count += 1

print(count/len(data)*100)
