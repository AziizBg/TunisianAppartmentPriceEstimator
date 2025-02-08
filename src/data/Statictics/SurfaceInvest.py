import json

# Load the dataset
file_path = "../../../data/PreProcessed/Treated.json"
output_file_path = "SurfacesHigherThan300.json"

data = []
try:
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    print("JSON file is valid.")
except json.JSONDecodeError as e:
    print(f"JSONDecodeError: {e.msg} at line {e.lineno}, column {e.colno}")

# Extract unique surface values
surface_values = set()

for entry in data:
    if 'surface' in entry and entry['surface'] is not None:
        surface_values.add(entry['surface'])

# Sort the unique surface values
unique_surface_values = sorted(surface_values)

# Count surfaces higher than 300
higher_than_300_count = sum(1 for value in unique_surface_values if value > 300)
higher_than_300_values = [value for value in unique_surface_values if value > 300]
records_higher_than_300 = [
    entry for entry in data if 'surface' in entry and entry['surface'] is not None and entry['surface'] > 600
]
# Print the unique surface values and the count of values > 200
print("Unique Surface Values:")
print(unique_surface_values)
print(f"Number of surfaces higher than 300: {higher_than_300_count}")


with open(output_file_path, "w", encoding="utf-8") as file:
    json.dump(records_higher_than_300, file, ensure_ascii=False, indent=4)

with open(output_file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

print(len(data))