import json
import re

# Load the dataset
file_path = "../../../data/PreProcessed/Treated.json"

with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# Total entries
total_entries = len(data)

with_surface = 0
without_surface = 0
extracted_surface_count = 0

# Collect entries without surface and try to extract from the description
entries_without_surface = []
surface_pattern = re.compile(r"surface en m²\s*:\s*(\d+)", re.IGNORECASE)

for entry in data:
    if 'surface' in entry and entry['surface'] is not None:
        with_surface += 1
    else:
        without_surface += 1
        # Try to extract surface from the description if it exists

        if 'description' in entry:
            match = surface_pattern.search(entry['description'])
            if match:
                extracted_surface = int(match.group(1))
                entry['surface'] = extracted_surface
                extracted_surface_count += 1
                # print(f"Extracted surface {extracted_surface} for entry: {entry}")
            else:
                print(f" Without: {entry}")
                entries_without_surface.append(entry)

# Calculate percentages
with_surface_percentage = (with_surface / total_entries) * 100 if total_entries > 0 else 0
without_surface_percentage = (without_surface / total_entries) * 100 if total_entries > 0 else 0

# Display results
print(f"Entries with surf: {with_surface} ({with_surface_percentage:.2f}%)")
print(f"Entries without surf: {without_surface} ({without_surface_percentage:.2f}%)")
print(f"Number of newly extracted surf values: {extracted_surface_count}")

# Write the updated data to a new JSON file
with open(file_path, "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)
