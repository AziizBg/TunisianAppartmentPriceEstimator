import json

with open('data/processed/CleanedProcessed.json', 'r', encoding="utf-8") as file:
    data = json.load(file)

count = 0
for item in data:
    if 'description' in item.keys():
        if 'garage' in item['description'].lower():
            item['garage'] = 'yes'
            count += 1
        else:
            item['garage'] = 'no'

with open('data/processed/CleanedProcessed.json', 'w', encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print(count/len(data)*100)
