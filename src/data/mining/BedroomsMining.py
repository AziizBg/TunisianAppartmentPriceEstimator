import json
import re

# Load the dataset
file_path = "../../../data/PreProcessed/Treated.json"
output_file_path = "updated_binded_bedrooms.json"

with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# Patterns to match bedroom information
pattern1 = re.compile(r"s\+\s*(\d+)", re.IGNORECASE)  # "s+" followed by a number
pattern2 = re.compile(r"\s+s([0-4])", re.IGNORECASE)  # space followed by "s" and a number from 0 to 4
pattern3 = re.compile(r"(\d+)\s*(chambres?|chambre)", re.IGNORECASE)  # "2chambre", "3 chambres" (with or without space)

# Counter for extracted bedrooms
extracted_bedrooms_count = 0
no_bedrooms_count = 0

for entry in data:
    # Extract bedroom count from description if the field is missing
    if 'bedrooms' not in entry or entry['bedrooms'] is None:
        if 'description' in entry:
            match1 = pattern1.search(entry['description'])
            match2 = pattern2.search(entry['description'])
            match3 = pattern3.search(entry['description'])
            if match1:
                extracted_bedrooms = int(match1.group(1))
                entry['bedrooms'] = extracted_bedrooms
                extracted_bedrooms_count += 1
            elif match2:
                extracted_bedrooms = int(match2.group(1))
                entry['bedrooms'] = extracted_bedrooms
                extracted_bedrooms_count += 1
            elif match3:
                extracted_bedrooms = int(match3.group(1))
                entry['bedrooms'] = extracted_bedrooms
                extracted_bedrooms_count += 1
            else:
                no_bedrooms_count += 1
                print("No pattern matched for entry:", entry)

# Display the number of extracted bedroom values
print(f"Number of newly extracted bedroom values: {extracted_bedrooms_count}")
print(f"Number of no bedrooms values: {no_bedrooms_count}")

# Write the updated data to a new JSON file
with open(output_file_path, "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)
