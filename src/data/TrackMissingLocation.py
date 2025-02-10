import json
import pandas as pd

# Charger le dataset
with open('data/processed/processed.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Mots-clés à rechercher
keywords = ["mourouj 6", "mourouj6"]

# Stocker les enregistrements correspondants
matched_records = []

# Parcourir le dataset
for i, record in enumerate(data):
    location = record.get("location", "").lower()
    description = record.get("description", "").lower()

    # Vérifier si "mourouj 6" ou "mourouj6" sont présents
    if any(keyword in location or keyword in description for keyword in keywords):
        matched_records.append({
            "Index": i,
            "Location": record.get("location", ""),
            "Description": record.get("description", "")
        })

# Convertir les résultats en DataFrame pour affichage
df = pd.DataFrame(matched_records)

# Afficher les résultats sous forme de tableau
if not df.empty:
    print(df.to_string(index=False))
else:
    print("❌ Aucun enregistrement trouvé contenant 'mourouj 6' ou 'mourouj6'.")

# Sauvegarder les résultats dans un fichier JSON
with open('data/PreProcessed/Mourouj6_ExactMatches.json', 'w', encoding='utf-8') as f:
    json.dump(matched_records, f, indent=2, ensure_ascii=False)

with open('data/PreProcessed/RiadhDescriptions.json', 'w', encoding='utf-8') as f:
    json.dump(df["Description"].tolist(), f, indent=2, ensure_ascii=False)

print("✅ Extraction terminée. Résultats sauvegardés dans 'Mourouj6_ExactMatches.json'.")
