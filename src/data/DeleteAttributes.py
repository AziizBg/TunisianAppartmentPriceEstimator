import json

# File paths
input_file = '../../data/processed/processed.json'
output_file = '../../data/processed/CleanedProcessed.json'

# Attributes to remove
# to delete next step:  "description"
attributes_to_remove = ["age", "Etat", "date", "location", "floor_description", "rooms"]

# Load JSON data with UTF-8 encoding
with open(input_file, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Remove specified attributes from each record
for record in data:
    for attribute in attributes_to_remove:
        record.pop(attribute, None)

# Save the cleaned data with UTF-8 encoding
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print(f"Cleaned data saved to {output_file}")
