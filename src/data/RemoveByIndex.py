import json

# Charger les données
with open('data/processed/CleanedProcessed.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Liste des index à supprimer (triés en ordre décroissant pour éviter les décalages)
indexes_to_remove = sorted([2874, 3263, 4101, 4882, 5377, 6467, 6868, 8251, 8698], reverse=True)

# Suppression des enregistrements
for idx in indexes_to_remove:
    if idx < len(data):
        del data[idx]
    else:
        print(f"Index {idx} hors limites - non supprimé")

# Sauvegarder les données modifiées
with open('data/processed/CleanedProcessed.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"{len(indexes_to_remove)} enregistrements supprimés avec succès")