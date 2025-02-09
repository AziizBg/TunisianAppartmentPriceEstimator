import json

def find_price_outliers(data):
    """Trouve les indices des prix > 3 000 000 ou < 40 000"""
    outliers = []
    
    for idx, record in enumerate(data):
        try:
            price = record['price']
            
            # Vérifier si le prix est numérique
            if not isinstance(price, (int, float)):
                continue
                
            # Vérifier les conditions
            if price >= 3000000 or price <= 40000:
                outliers.append((idx, record))
                
        except KeyError:
            continue  # Ignorer les entrées sans clé 'price'
    
    return outliers

# Charger les données nettoyées
with open('data/processed/CleanedProcessed.json', 'r', encoding='utf-8') as f:
    cleaned_data = json.load(f)

# Trouver les outliers
# outlier_records = find_price_outliers(cleaned_data)

# Afficher les résultats
# print(f"{len(outlier_records)} anomalies trouvées :")
# print("Indices concernés :", [idx for idx, _ in outlier_records])

# Optionnel: Sauvegarder les indices et les enregistrements
# with open('price_outliers.json', 'w', encoding='utf-8') as f:
#     json.dump(outlier_records, f, indent=2, ensure_ascii=False)

def change_price_outliers():
    # Charger vos données nettoyées (exemple de structure)
    CleanedProcessedGt3000000Sm40000 = {
        600: 520000,       
        654: 760000,       
        710: 3000000,       
        733: 98218,       
        817: 3000000,       
        929: 780000,       
        938: 350000,       
        1585: 3000000,      
        1990: 587000,      
        2310: 40000,      
        2311: 400000,      
        2312: 40000,      
        2604: 350000,      
        2874: 30000,   # a supprimer  
        2875: 3000000,      
        3071: 270000,      
        3262: 250000,      
        3263: 25000, # a supprimer      
        3454: 230000,      
        3654: 200000,      
        4101: 15000,   # a supprimer
        4102: 150000,      
        4340: 111111,      
        4368: 100000,      
        4587: 380000,      
        4618: 350000,      
        4764: 247000,      
        4882: 18000,    # a supprimer   
        4952: 260000,      
        5037: 100000,      
        5038: 100000,      
        5039: 1000000,      
        5111: 65000,      
        5377: 25000, # a supprimer        
        5696: 425000,      
        5746: 222220,      
        5932: 587000,      
        5943: 320000,     
        6091: 255000,      
        6092: 190000,      
        6097: 3100000,      
        6463: 120000,      
        6467: 9500000,   # a supprimer
        6537: 650000,      
        6868: 10666, # a supprimer      
        6958: 222220,      
        7104: 320000,      
        7204: 587000,      
        7241: 255000,      
        7242: 190000,      
        7246: 3100000,      
        7628: 120000,      
        7896: 3000000,      
        7973: 380000,      
        7998: 310000,      
        8025: 570000,      
        8102: 380000,      
        8108: 235000,      
        8123: 280000,      
        8124: 290000,      
        8125: 280000,     
        8127: 235000,      
        8143: 330000,      
        8251: 352000, # a supprimer
        8281: 80000,      
        8451: 3100000,      
        8523: 330000,      
        8597: 230000,      
        8698: 28000 # a supprimer
    }
    CleanedProcessed = {
        15: 158000,
        151: 220000,
        1110: 270000,
        5193: 120000,
        5215: 150000,
        6360: 205000,
        6613: 150000,
        8048: 130000,
        8410: 200000,
        8656: 255000
    }


    # Charger les données originales
    with open('data/processed/CleanedProcessed.json', 'r', encoding='utf-8') as f:
        records = json.load(f)

    # Boucler et corriger les prix
    for index, record in enumerate(records):
        if index in CleanedProcessed:
            # Appliquer votre correction manuelle
            record['price'] = CleanedProcessed[index]
            
            # Optionnel: logger les changements
            print(f"Correction enregistrement {index}:")
            print(f"Ancien prix: {record.get('price', 'N/A')} => Nouveau prix: {CleanedProcessed[index]}")
        else:
            print(f"Aucune correction pour l'enregistrement {index}")

    # Sauvegarder les modifications
    with open('data/processed/CleanedProcessed.json', 'w', encoding='utf-8') as f:
        json.dump(records, f, indent=2, ensure_ascii=False)

    print("Correction terminée. Résultats sauvegardés dans CleanedProcessed.json")

# Appeler la fonction
# change_price_outliers()