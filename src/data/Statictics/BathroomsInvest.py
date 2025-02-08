import json

# Load the dataset
file_path = "../../../data/processed/CleanedProcessed.json"

with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

without_bathrooms = 0
for entry in data:
    if 'bathrooms' not in entry or entry['bathrooms'] is None:
        without_bathrooms += 1
        print(entry)

print(without_bathrooms)