import json
import statistics

# Load the dataset
file_path = "../../data/PreProcessed/Treated.json"
output_file_path = "../../data/PreProcessed/Treated.json"

with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# Initialize counters
with_bathrooms = 0
without_bathrooms = 0

one_bathroom = 0
two_bathrooms = 0
three_bathrooms = 0


# Total entries
total_entries = len(data)

# Count entries
for entry in data:
    if 'bathrooms' in entry and entry['bathrooms'] is not None:
        with_bathrooms += 1
    else:
        # mine from the description attribute: look for the words 'bain', 'douches', 'salle de bain', 'salle de douche', 'salle d'eau', 'toilette', 'wc', 'lavabo', 'bidet', 'baignoire', 'douche'
        if 'description' in entry and entry['description'] is not None:
            description = entry['description'].lower()
            if 'salle de bain' in description or 'salle de douche' in description or 'salle d\'eau' in description or 'toilette' in description or 'baignoire' in description or 'douche' in description:
                with_bathrooms += 1
                one_bathroom += 1
                entry['bathrooms'] = 1
            
            # else if the description contains the word 'salles de bain' or 'salles de douche' or 'salles d'eau' or 'toilettes' or 'baignoires' or 'douches': we mine the number of bathrooms by looking for the number of bathrooms before the word in the description
            elif 'salles de bain' in description or 'salles de douche' in description or 'salles d\'eau' in description or 'toilettes' in description or 'baignoires' in description or 'douches' in description:
                with_bathrooms += 1
                entry['bathrooms'] = 2
                # get the number of bathrooms
                words = description.split()
                for i in range(len(words)):
                    if words[i] == 'salles'  or words[i] == 'toilettes' or words[i] == 'baignoires' or words[i] == 'douches':
                        if words[i-1].isdigit():
                            entry['bathrooms'] = int(words[i-1])
                            break
            elif 'bedrooms' in entry and entry['bedrooms'] is not None:
                # if the bedrooms are between 1 and 3, we assume that there is only one bathroom
                if entry['bedrooms'] >= 1 and entry['bedrooms'] <= 3:
                    with_bathrooms += 1
                    entry['bathrooms'] = 1
                    one_bathroom += 1
                # if the bedrooms are between 4 and 6, we assume that there are two bathrooms
                elif entry['bedrooms'] >= 4 and entry['bedrooms'] <= 6:
                    with_bathrooms += 1
                    entry['bathrooms'] = 2
                    two_bathrooms += 1
                # if the bedrooms are greater than 6, we assume that there are three bathrooms
                elif entry['bedrooms'] > 6 and entry['bedrooms'] <= 9:
                    with_bathrooms += 1
                    entry['bathrooms'] = 3
                    three_bathrooms += 1
            else:                
                without_bathrooms += 1

# Calculate percentages
with_bathrooms_percentage = (with_bathrooms / total_entries) * 100 if total_entries > 0 else 0
without_bathrooms_percentage = (without_bathrooms / total_entries) * 100 if total_entries > 0 else 0

# Display results
print(f"Entries with bathrooms: {with_bathrooms} ({with_bathrooms_percentage:.2f}%)")
print(f"Entries without bathrooms: {without_bathrooms} ({without_bathrooms_percentage:.2f}%)")

# print stats about the number of bathrooms and the percent of entries with bathrooms
print(f"Added entries with 1 bathroom: {one_bathroom}")
print(f"Added entries with 2 bathrooms: {two_bathrooms}")
print(f"Added entries with 3 bathrooms: {three_bathrooms}")




# Write the updated data to a new JSON file
with open(output_file_path, "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print(f"Updated dataset saved to {output_file_path}")
# print(f"Median value used for bedrooms replacement: {median_bedrooms}")
