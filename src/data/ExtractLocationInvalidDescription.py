import json

def extract_descriptions_by_municipality(data, municipality, valid_locations):
    descriptions = []
    print(f"🔹 Extraction des descriptions pour {municipality}...")
    print(f"🔹 Locations valides: {valid_locations}")
    for record in data:
        if record.get("municipality") == municipality:
            location = record.get("location", "")

            # Vérifier si la location est dans la liste (en ignorant la casse et les espaces)
            if any(location == loc for loc in valid_locations):
                description = record.get("description")
                if description:
                    descriptions.append(description)

    return descriptions

# Chargement des données JSON
with open('data/processed/processed.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"🔹 Chargé {len(data)} enregistrements.")

# Liste des locations valides
valid_locations = [
    "Tunis",
    "Carthage",
    "Tunis  -  Carthage",
    "hshainzaghouannord@gmail.com, Carthage, Tunis",
    "Carthage, Tunis",
    "carthage yasmina, Carthage, Tunis"
]

# Extraction des descriptions
result = extract_descriptions_by_municipality(data, "EL YASMINA", valid_locations)

# Sauvegarde des résultats dans un fichier JSON
output_path = 'data/PreProcessed/RiadhDescriptions.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print(f"✅ {len(result)} descriptions extraites et sauvegardées dans {output_path}")


# Load the dataset
with open('data/processed/CleanedProcessed.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Load the extracted descriptions
with open('data/PreProcessed/RiadhDescriptions.json', 'r', encoding='utf-8') as f:
    descriptions = json.load(f)

# Find the index of each description in the dataset
for desc in descriptions:
    index = next((i for i, record in enumerate(data) if record.get("description") == desc), "n'existe pas")
    print(f"Description: {desc}\n➡ Index: {index}\n")
