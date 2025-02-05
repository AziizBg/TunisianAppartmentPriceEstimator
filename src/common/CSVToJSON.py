import csv
import json
import os

folder_path = ""
file_names = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
full_data = []

for file_name in file_names:
    data = []
    headers = []
    with open(folder_path+file_name, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            for header in row:
                headers.append(header)
            break
        for row in reader:
            item = {}
            for i in range(0, len(row)):
                if row[i] is not '':
                    item[headers[i]] = row[i]
                else:
                    item[headers[i]] = "N/A"
            data.append(item)
        file.close()
        with open('../../data/RAW'+file_name.replace("csv", "json"), 'w', encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        print(file_name, ":", len(data))
