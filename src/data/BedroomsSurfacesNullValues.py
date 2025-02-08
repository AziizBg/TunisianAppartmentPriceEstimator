import json
import statistics

# Load the dataset
file_path = "../../data/PreProcessed/Treated.json"

with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# Initialize counters
with_bedrooms = 0
without_bedrooms = 0

# Total entries
total_entries = len(data)
print(total_entries)
# Count entries
for entry in data:
    if 'bedrooms' in entry and entry['bedrooms'] is not None:
        with_bedrooms += 1
    else:
        without_bedrooms += 1

# Calculate percentages
with_bedrooms_percentage = (with_bedrooms / total_entries) * 100 if total_entries > 0 else 0
without_bedrooms_percentage = (without_bedrooms / total_entries) * 100 if total_entries > 0 else 0

# Display results
print(f"Entries with bedrooms: {with_bedrooms} ({with_bedrooms_percentage:.2f}%)")
print(f"Entries without bedrooms: {without_bedrooms} ({without_bedrooms_percentage:.2f}%)")


with_surface = 0
without_surface = 0
for entry in data:
    if 'surface' in entry and entry['surface'] is not None:
        with_surface += 1
    else:
        without_surface += 1

# Calculate percentages
with_surface_percentage = (with_surface / total_entries) * 100 if total_entries > 0 else 0
without_surface_percentage = (without_surface / total_entries) * 100 if total_entries > 0 else 0

# Display results
print(f"Entries with bedrooms: {with_surface} ({with_surface_percentage:.2f}%)")
print(f"Entries without bedrooms: {without_surface} ({without_surface_percentage:.2f}%)")


# Extract valid bedroom values (non-null)
bedroom_values = [entry['bedrooms'] for entry in data if 'bedrooms' in entry and entry['bedrooms'] is not None]
unique_bedroom_values = set(bedroom_values)
print("Unique bedroom values:", unique_bedroom_values)

# Calculate the median
median_bedrooms = statistics.median(bedroom_values) if bedroom_values else 0

# Replace null values for bedrooms with the median
for entry in data:
    if 'bedrooms' not in entry or entry['bedrooms'] is None:
        entry['bedrooms'] = median_bedrooms

# Create a dictionary to store surfaces by number of bedrooms
bedroom_surface_mapping = {}

for entry in data:
    bedrooms = entry['bedrooms']
    surface = entry.get('surface')

    if surface is not None:
        if bedrooms not in bedroom_surface_mapping:
            bedroom_surface_mapping[bedrooms] = []
        bedroom_surface_mapping[bedrooms].append(surface)

# Compute the mean surface for each bedroom group
bedroom_mean_surface = {
    bedrooms: statistics.mean(surfaces) for bedrooms, surfaces in bedroom_surface_mapping.items()
}

print("Mean surfaces per bedroom count:", bedroom_mean_surface)

# Replace null surface values with the corresponding mean
for entry in data:
    if entry.get('surface') is None:
        bedrooms = entry['bedrooms']
        entry['surface'] = bedroom_mean_surface.get(bedrooms, 0)  # Default to 0 if no mean available

# Write the updated data to a new JSON file
with open(file_path, "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print(f"Updated dataset saved to {file_path}")
print(f"Median value used for bedrooms replacement: {median_bedrooms}")