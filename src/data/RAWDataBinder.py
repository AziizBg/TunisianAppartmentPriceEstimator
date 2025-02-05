import json
import os

folder_path = "../../data/RAW"
file_names = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
full_data = []

for file_name in file_names:
    print(f"Loading {file_name}")
    with open('../../data/RAW/'+file_name, 'r', encoding="utf-8") as file:
        data = json.load(file)
        print(f"Loaded {file_name}, {len(data)}")
        full_data.extend(data)

print(len(full_data))
with open('../../data/PreProcessed/FULL0.json', 'w', encoding="utf-8") as file:
    json.dump(full_data, file, indent=4, ensure_ascii=False)
