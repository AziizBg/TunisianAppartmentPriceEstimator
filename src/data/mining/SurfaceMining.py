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

# Define separate regex patterns
patterns = [
    ("Pattern 1 (surface en m²:)", re.compile(r"surface en m²\s*:\s*(\d+)", re.IGNORECASE)),
    ("Pattern 2 (superficie 180 m)", re.compile(r"superficie\s+(\d+(?:\.\d+)?)\s*m", re.IGNORECASE)),
    ("Pattern 3 (superficie de 31m)", re.compile(r"superficie\s+de\s+(\d+(?:\.\d+)?)\s*m", re.IGNORECASE)),
    ("Pattern 4 (superficie de 98)", re.compile(r"superficie\s+de\s+(\d+(?:\.\d+)?)", re.IGNORECASE)),
    ("Pattern 5 (Superficie : 130)", re.compile(r"superficie\s*:\s*(\d+(?:\.\d+)?)", re.IGNORECASE)),
    ("Pattern 6 (superficie totale de 172)", re.compile(r"superficie totale de\s+(\d+(?:\.\d+)?)", re.IGNORECASE)),
    ("Pattern 7 (superficie totale de 242.5m)", re.compile(r"superficie totale de\s+(\d+(?:\.\d+)?)\s*m", re.IGNORECASE)),
    ("Pattern 8 (superficie totale de 100)", re.compile(r"superficie totale de\s+(\d+(?:\.\d+)?)", re.IGNORECASE)),
    ("Pattern 9 (superficie 176.40)", re.compile(r"superficie\s+(\d+(?:\.\d+)?)", re.IGNORECASE)),
    ("Pattern 10 (62 m de superficie)", re.compile(r"(\d+(?:\.\d+)?)\s*m\s+de superficie", re.IGNORECASE)),
    ("Pattern 11 (242 mètres carrés de superficie)", re.compile(r"(\d+(?:\.\d+)?)\s*mètres?\s+carrés?\s+de superficie", re.IGNORECASE)),
    ("Pattern 12 (Superficie totale 128m)", re.compile(r"superficie totale\s+(\d+(?:\.\d+)?)\s*m", re.IGNORECASE)),
]

for entry in data:
    if 'surface' in entry and entry['surface'] is not None:
        with_surface += 1
    else:
        without_surface += 1

        # Try to extract surface from the description if it exists
        if 'description' in entry:
            for pattern_name, pattern in patterns:
                match = pattern.search(entry['description'])
                if match:
                    extracted_surface = float(match.group(1))
                    entry['surface'] = extracted_surface
                    extracted_surface_count += 1
                    # print(f"extracted_surface: {extracted_surface}, {pattern_name} matched: {entry['description']}")
                    break
            else:
                entries_without_surface.append(entry)
                print(f"not matched: {entry['description']}")
# Calculate percentages
with_surface_percentage = (with_surface / total_entries) * 100 if total_entries > 0 else 0
without_surface_percentage = (without_surface / total_entries) * 100 if total_entries > 0 else 0

# Display results
print(f"Entries with surface: {with_surface} ({with_surface_percentage:.2f}%)")
print(f"Entries without surface: {without_surface} ({without_surface_percentage:.2f}%)")
print(f"Number of newly extracted surface values: {extracted_surface_count}")

# Write the updated data to a new JSON file
with open(file_path, "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)
