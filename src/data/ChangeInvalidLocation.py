import json
import pandas as pd

# Load the dataset
with open('data/processed/CleanedProcessed.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Load the extracted descriptions
with open('data/PreProcessed/RiadhDescriptions.json', 'r', encoding='utf-8') as f:
    descriptions = json.load(f)

# Store matched indexes
matched_records = []

# Update dataset where descriptions match
for i, record in enumerate(data):
    if record.get("description") in descriptions:
        matched_records.append({"Index": i, "Description": record["description"]})
        
        # Update record
        record["state"] = "TUNIS"
        record["delegation"] = "CARTHAGE"
        record["municipality"] = "CARTHAGE EL YASMINA"

# Convert matched records to a DataFrame for a table output
df = pd.DataFrame(matched_records)

# Print the table
if not df.empty:
    print(df.to_string(index=False))
else:
    print("No matching records found.")

# Save the updated dataset
with open('data/processed/CleanedProcessed.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("✅ Dataset updated and saved ")
