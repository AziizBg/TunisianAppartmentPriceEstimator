import json
import math
import re
from text_to_num import alpha2digit
from difflib import SequenceMatcher

with open('../../data/RAW/Binded.json', 'r', encoding="utf-8") as file:
    data = json.load(file)

with open('../../data/GeoData/Locations.json', 'r', encoding="utf-8") as file:
    locationdata = json.load(file)

states_dict = {}
delegation_states = {}
state_delegations = {}
delegation_munips = {}
munips_delegations = {}
states = []
delegations = []
munips = []
states_dict['Default'] = []
Reverse_States = {}
for item in locationdata:
    states.append(item['governorate'].upper())
    states_dict['Default'].append(item['governorate'].upper())
    Reverse_States[item['governorate'].upper()] = 'Default'
    state_delegations[item['governorate'].upper()] = []
    for delegation in item['delegations']:
        delegations.append(delegation['delegation'].upper())
        delegation_munips[delegation['delegation'].upper()] = []
        state_delegations[item['governorate'].upper()].append(delegation['delegation'].upper())
        delegation_states[delegation['delegation'].upper()] = item['governorate'].upper()
        for munip in delegation['localities']:
            munips.append(munip)
            delegation_munips[delegation['delegation'].upper()].append(munip)
            munips_delegations[munip] = delegation['delegation'].upper()


def show_all_valid_records(col, db):
    for db_item in db:
        if col in db_item.keys():
            if db_item[col] != 'N/A':
                print(db_item[col])


def show_record_options(col, db):
    recs = {}
    for db_item in db:
        if col in db_item.keys():
            if db_item[col] in recs.keys():
                recs[db_item[col]] += 1
            else:
                recs[db_item[col]] = 1
    return recs


def show_overlapping_records(cols, db):
    res = []
    for db_item in db:
        data_snap = {}
        found = True
        for col in cols:
            if col not in db_item.keys():
                found = False
                break
            if db_item[col] == "N/A":
                found = False
                break
            data_snap[col] = db_item[col]
        if found:
            res.append(data_snap)
            print(data_snap)
    return res


def exists(col, record):
    if col in record.keys():
        if record[col] != 'N/A':
            return True
    return False


def exists_and_equal(col, value, record):
    if exists(col,record):
        if float(record[col]) == float(value):
            return True
    return False


def match_Word_Pattern(item, col, pattern):
    pattern_Match = re.search(pattern, item['description'].lower())
    if pattern_Match:
        item[col] = 'Yes'


def match_Closest_Word(item_text, wordlist):
    matches = []
    for word in wordlist:
        phrase_words = len(word.split())
        words_in_text = item_text.split()
        max = 0
        for i in range(len(words_in_text) - phrase_words + 1):
            substring = " ".join(words_in_text[i:i + phrase_words])
            similarity = SequenceMatcher(None, word, substring).ratio()
            if similarity > max:
                max = similarity
            if similarity == 1:
                break
        matches.append(max)
        if max == 1:
            break
    res = {}
    max = 0
    for i in range(len(matches)):
        if matches[i] > matches[max]:
            max = i
    res[wordlist[max]] = matches[max]
    return res


def location_Mapper(location_Levels, location_level_lookup, flat_location_levels, location_Level_Names, location_cols, dbItem):
    previousLevelOptimization = None
    for i in range(len(location_Level_Names)):
        dbItem[location_Level_Names[i] + 'Report'] = 0
        for location_col in location_cols[i]:
            if exists(location_col, dbItem):
                if previousLevelOptimization is not None:
                    potential_matches = match_Closest_Word(dbItem[location_col].upper(), location_Levels[i][previousLevelOptimization])
                else:
                    potential_matches = match_Closest_Word(dbItem[location_col].upper(), flat_location_levels[i])
                best = next(iter(potential_matches.items()))
                if best[1] > dbItem[location_Level_Names[i] + 'Report']:
                    dbItem[location_Level_Names[i] + 'Report'] = best[1]
                    dbItem[location_Level_Names[i]] = best[0]
                if math.isclose(dbItem[location_Level_Names[i] + 'Report'], 1.0, rel_tol=1e-9, abs_tol=0.0):
                    break
        if math.isclose(dbItem[location_Level_Names[i] + 'Report'], 1.0, rel_tol=1e-9, abs_tol=0.0):
            previousLevelOptimization = dbItem[location_Level_Names[i]]
        else:
            previousLevelOptimization = None


change = [
    ['prix', 'price'],
    ['texte', 'description'],
    ['Titre', 'title'],
    ['name', 'title'],
    ['gouvernorat', 'state'],
    ['lieu', 'state'],
    ['Année de construction', 'construction year'],
    ['Année construction', 'construction year'],
    ['annee de construction', 'construction year'],
    ['nombre de chambre', 'bedrooms'],
    ['Chambre', 'bedrooms'],
    ['chambres', 'bedrooms'],
    ['Chambres', 'bedrooms'],
    ['type', 'rooms'],
    ['Pièces', 'rooms'],
    ['nombre de pièces', 'rooms'],
    ['Piéces (Totale)', 'rooms'],
    ['nombre de salles de bain', 'bathrooms'],
    ['Salle de bain', 'bathrooms'],
    ['salle de bains', 'bathrooms'],
    ['Salles de bains', 'bathrooms'],
    ['surface_constructible', 'surface'],
    ['area', 'surface'],
    ['superficie', 'surface'],
    ['Superficie', 'surface'],
    ['Surface', 'surface'],
    ['Surf habitable', 'surface'],
    ['etage', 'floor'],
    ["Nombre d'étages", 'floor'],
    ['Étage du bien', 'floor'],
    ['étage', 'floor'],
    ['build_year', 'construction year'],
    ['taille', 'surface'],
    ['Standing', 'category'],
    ['Catégorie', 'category'],
    ['Chauffage central', 'heating'],
    ['Chauffage centrale', 'heating'],
    ['Chauffage électriques', 'heating'],
    ['chauffage central', 'heating'],
    ['places_parking', 'parking'],
    ['Parking', 'parking'],
    ['Ascenseur', 'elevator'],
    ['Place de parc', 'parking'],
    ['Climatisation', 'air_conditioning'],
    ['air conditionné', 'air_conditioning'],
    ['Sécurité', "security"],
    ['sécurité', "security"],
    ['concierge', 'security'],
    ['Concierge', 'security'],
    ['système de sécurité', 'security'],
    ['24/7 securité', 'security'],
    ["système d'alarme", 'security'],
    ['Système Alarme', 'security'],
    ['place parking', 'parking'],
    ['chauffage au sol', 'heating'],
    ['chauffage', 'heating'],
    ['climatisation', 'air_conditioning'],
    ['camera de sécurité', 'security'],
    ['Garage', 'garage'],
    ['garages', 'garage'],
    ['Terrasse', 'balcony'],
    ['Terrasses', 'balcony'],
    ['terrasse', 'balcony'],
    ['balcon', "balcony"],
    ['ascenseur', 'elevator'],
    ['double ascenseurs', 'elevator'],
    ['Meublée', 'furniture'],
    ['Meublé', 'furniture'],
    ['meublé', 'furniture'],
    ['Cuisine équipée', 'equipped_kitchen'],
    ['cuisine équipée', 'equipped_kitchen'],
    ['Cuisine équipé', 'equipped_kitchen'],
    ['Double vitrage', 'double vitrage'],
    ['Etat du bien', "age"],
    [' chauffage central', 'heating'],
    ['✔️ chauffage central', 'heating'],
    ['Municipalité', 'municipality'],
    ['localite', 'municipality']
]
to_delete = [
    'Région',
    "Vendeur",
    "gallery-transtype",
    "texte-annnonce",
    "Chambre rangement",
    "État",
    "Salon européen",
    "Surf terrain",
    "Adresse",
    "nombre_etages",
    "address",
    "free",
    "Orientation",
    "orientation",
    "longitude",
    "latitude",
    "Disponible le",
    "Type du sol",
    "metres carres habitables",
    "Appartement",
    "Livraison",
    "Année de restructuration interne",
    "Parabole / TV",
    "renovation_year",
    "Construction conventionnelle",
    "Interphone",
    "Micro-ondes",
    "Antenne parabolique",
    "Postal Code",
    'Type de bien',
    'cmpdisc'
]

joins = [
]

location_Sawp = [
    ["ariana essoghra", "ariana essoughra"],
    ["ariana esoghra", "ariana essoughra"],
    ['ariana soughra', "ariana essoughra"],
    ["petite ariana", "ariana essoughra"],
    ["riadh andlous", "riadh el andalous "],
    ["riadh andalous", "riadh el andalous "],
    ["Ennekilette", "Nkhilet"],
    ['Ennkhilette', "Nkhilet"],
    ["ennkhilet", "Nkhilet"],
    ["enkhillette", "Nkhilet"],
    ["enkhilet", "Nkhilet"],
    ["enkhilette", "Nkhilet"],
    ["borj twil", "borj touil"],
    ["Cité Ettahrir", "Ettahrir 1"],
    ["Zone urbaine nord", "Centre Urbain Nord"],
    ["حي إبن سيناء", "Ibn Sina"],
    ["wahat","Cité les palmeraies"],
    ["cite wahat","Cité les palmeraies"],
    ["cité el wahat ","Cité les palmeraies"],
    ["hay el wahat","Cité les palmeraies"],
    ["Cite Erriadh","Marsa Erriadh"],
    ["Meghira Centre","El Mghira"],
    ["Medina Jedida","Nouvelle Medina"],
    ["Monfleury","Montfleury"],
    ["Hadika","Cite Du Jardin"]
]
price_bounds = [10000, 1000000000]

'''to_del = []
count = 0
for i in range(len(data)):
    count += 1
    if count%100==0:
        print(f"{count}/{len(data)}")
    if 'description' not in data[i].keys():
        continue
    if data[i]['description'] == 'N/A':
        continue
    if not exists('cmpdisc', data[i]):
        data[i]['cmpdisc'] = data[i]['description'].replace(' ', '').replace('\n', '').replace('\r', '').replace('  ', '')
    for j in range(i+1, len(data)):
        if 'description' not in data[j].keys():
            continue
        if data[j]['description'] == 'N/A':
            continue
        if not exists('cmpdisc', data[j]):
            data[j]['cmpdisc'] = data[j]['description'].replace(' ', '').replace('\n', '').replace('\r', '').replace('  ', '')
        if data[i]['cmpdisc'] == data[j]['cmpdisc']:
            if data[j] not in to_del:
                to_del.append(data[j])
print(f'Found {len(to_del)} repeat records')

for d_item in to_del:
    while d_item in data:
        data.remove(d_item)
    data.append(d_item)
'''
counter = 0
to_del = []
lcheck = 0
print(len(data))
for item in data:
    lcheck += 1
    if lcheck % 100 == 0:
        print(f'{lcheck}|{len(data)}')
    if lcheck % 100 == 0:
        with open(f'../../data/PreProcessed/Treated.json', 'w', encoding="utf-8") as file:
             json.dump(data, file, indent=4, ensure_ascii=False)
    # location name sawp
    if exists("description", item):
        for sawp in location_Sawp:
            item["description"] = item["description"].replace(sawp[0], sawp[1])
        item["description"] = re.sub(r'\s+', ' ', item["description"])
    # location treatment
    location_Mapper([states_dict, state_delegations, delegation_munips], [Reverse_States, delegation_states, munips_delegations], [states, delegations, munips],
                ['NewState', 'NewDelegation', 'newMunip'],
                [
                    ['state', 'location', 'description'],
                    ['delegation', 'location', 'description'],
                    ['municipality', 'location', 'description']
                ], item)
    '''
    # caracteristiques flattening
    if 'caracteristiques' in item.keys():
        if item['caracteristiques'] != 'N/A':
            caracteristics = item['caracteristiques'].replace('Equipements', ',Equipements').split(',')
            for car in caracteristics:
                car_split = car.strip().split(':')
                if 'près' in car.lower():
                    continue
                if len(car) > 20:
                    continue
                if len(car_split) == 1:
                    if 'm²' in car_split[0] and 'surface' not in item.keys():
                        item['surface'] = car_split[0]
                    elif 'standing' in car_split[0]:
                        item['category'] = car_split[0]
                    else:
                        item[car_split[0].lower().replace('-', '')] = 'Yes'
                elif len(car_split) == 2:
                    item[car_split[0].lower().replace('-', '')] = car_split[1].replace('-', '')
                elif 'LIVRAISON' not in car.upper():
                    print("NO WAY: ", car)
            del item['caracteristiques']
    # item deletions
    for elete in to_delete:
        if elete in list(item.keys()):
            del item[elete]
    # joins
    for join in joins:
        if not exists(join[1], item) and join[0] in item.keys():
            item[join[1]] = item[join[0]]
            del item[join[0]]
        elif join[0] in item.keys() and join[1] in item.keys():
            if item[join[0]] != 'N/A':
                item[join[1]] += '+' + item[join[0]]
            del item[join[0]]
    # Name changes
    for change_item in change:
        if change_item[0] in item.keys():
            if change_item[1] in item.keys():
                if change_item[1] != 'N/A':
                    del item[change_item[0]]
                    continue
            item[change_item[1]] = item[change_item[0]]
            counter += 1
            del item[change_item[0]]
    # Sous-type filter
    if 'Sous-type' in item.keys() and item['bedrooms'] == 'N/A':
        if item['Sous-type'].startswith('S+'):
            item['bedrooms'] = item['Sous-type'].replace('S+', '')
        del item['Sous-type']
    # unknown 1 & 2 filter
    if 'Unkwn 1' in item.keys() or 'Unkwn 0' in item.keys():
        room = None
        bedroom = None
        if item['Unkwn 1'] != 'N/A':
            if 'Chambre' in item['Unkwn 1']:
                bedroom = item['Unkwn 1'].replace('Chambre', '')
            if 'Pièce' in item['Unkwn 1']:
                room = item['Unkwn 1'].replace('Pièce', '')
        if item['Unkwn 0'] != 'N/A':
            if 'Chambre' in item['Unkwn 0']:
                bedroom = item['Unkwn 0'].replace('Chambre', '')
            if 'Pièce' in item['Unkwn 0']:
                room = item['Unkwn 0'].replace('Pièce', '')
        if bedroom is not None:
            if 'bedrooms' in item.keys():
                if item['bedrooms'] == 'N/A':
                    item['bedrooms'] = bedroom
            else:
                item['bedrooms'] = bedroom
        if room is not None:
            if 'rooms' in item.keys():
                if item['rooms'] == 'N/A':
                    item['rooms'] = room
            else:
                item['bedrooms'] = room
        del item['Unkwn 0']
        del item['Unkwn 1']
    # fixing age language
    if 'age' in item.keys():
        if item['age'] != 'N/A':
            if item["age"].lower() == "moins d'un an":
                item["age"] = "Less than a year"
            elif item["age"] == "1-5 ans":
                item["age"] = "1-5 years"
            elif item["age"] == "5-10 ans":
                item["age"] = "5-10 years"
            elif item["age"] == "10-20 ans":
                item["age"] = "10-20 years"
            elif item["age"] == '20-30 ans':
                item["age"] = "20-30 years"
            elif item["age"] == "30-50 ans":
                item["age"] = "30-50 years"
            elif item["age"] == "50-70 ans":
                item["age"] = "50-70 years"
            elif item["age"] == "70-100 ans":
                item["age"] = "70-100 years"
            else:
                item["age"] = "More than 100 years"
        else:
            del item['age']
    # price filter

    # construction year shift
    if 'construction year' in item.keys():
        if item['construction year'] != 'N/A':
            gap = 2024 - int(item['construction year'])
            if gap <= 1:
                item["age"] = "Less than a year"
            elif gap <= 5:
                item["age"] = "1-5 years"
            elif gap <= 10:
                item["age"] = "5-10 years"
            elif gap <= 20:
                item["age"] = "10-20 years"
            elif gap <= 30:
                item["age"] = "20-30 years"
            elif gap <= 50:
                item["age"] = "30-50 years"
            elif gap <= 70:
                item["age"] = "50-70 years"
            elif gap <= 100:
                item["age"] = "70-100 years"
            elif gap <= 200:
                item["age"] = "More than 100 years"
        del item['construction year']
    # clean surface
    if 'surface' in item.keys():
        if item['surface'] != 'N/A':
            try:
                item['surface'] = int(float(item['surface'].replace('m²', '').replace('m2', '').strip()))
            except:
                del item['surface']
    # price filtering
    if not exists('price', item):
        to_del.append(item)
    else:
        item['price'] = str(item['price']).replace(' ', '').replace('\xa0', '').lower()
        if 'prixsurdemande' in item['price'] or 'prixàconsulter' in item['price']:
            to_del.append(item)
        else:
            try:
                item['price'] = int(item['price']
                                    .lower()
                                    .replace('dt', '')
                                    .replace('.', '')
                                    .replace(',', '')
                                    .replace('tnd', '').strip())
                if item['price'] <= price_bounds[0] or item['price'] >= price_bounds[1]:
                    to_del.append(item)
            except:
                to_del.append(item)
    # description filling
    desc_found = exists('description', item)
    title_found = exists('title', item)
    if not desc_found:
        if title_found:
            item['description'] = item['title']
    elif desc_found and title_found:
        item['description'] += ' ' + item['title']
    if 'title' in item.keys():
        del item['title']
    if exists('rooms', item):
        try:
            float(item['rooms'].replace('+', ''))
            item['rooms'] = item['rooms'].replace('+','')
        except ValueError:
            if not exists('description', item):
                item['description'] = item['rooms']
            else:
                item['description'] += ' ' + item['rooms']
            del item['rooms']
    if exists('description', item):
        if not exists('bedrooms', item):
            match = re.search(r"s\+?\d+", item['description'].lower())
            match2 = re.search(r"\dchambre+", alpha2digit(item['description'].replace('>', ' ')
                                                          .replace('une chambre', '1 chambre'), 'fr')
                               .lower().replace(' ', '').replace('-', ' '))
            if match:
                item['bedrooms'] = match.group().replace('S', '').replace('+', '')
            if match2 and not match:
                item['bedrooms'] = match2.group().replace('chambre', '')
        if not exists('rooms', item):
            match = re.search(r"\d+\s*pièc+", item['description'].lower().replace(' ', '').replace('\n', ''))
            if match:
                item['rooms'] = match.group().replace('pièc', '')
        if not exists('surface', item):
            match = re.findall(r"\d+\s?(?:m2|m²)", item['description'].lower()
                               .replace(' ', '')
                               .replace('', ''))
            maximum = 0
            for sur in match:
                s = int(sur.replace('m²', '').replace('m2', ''))
                if s > maximum:
                    maximum = s
            if maximum > 0:
                item['surface'] = maximum
        if not exists('parking', item):
            match_Word_Pattern(item, 'parking', r'parking')
        if not exists('heating', item):
            match_Word_Pattern(item, 'heating', r'chauffage')
        if not exists('air_conditioning', item):
            match_Word_Pattern(item, 'air_conditioning', r'climatis')
        if not exists('garage', item):
            match_Word_Pattern(item, 'garage', 'garage')
        if not exists('balcony', item):
            match_Word_Pattern(item, 'balcony', "balcon")
            match_Word_Pattern(item, 'balcony', "terrasse")
    # state cleaning
    if exists('state', item):
        if 'AGO' in item['state'].upper():
            del item['state']
        else:
            item['state'] = item['state'].strip().capitalize()
    # bedroom cleaning
    if exists('bedrooms', item):
        if str(item['bedrooms']).isdigit():
            pass
        elif 'Pièce' in item['bedrooms']:
            if not exists('rooms', item):
                item['rooms'] = item['bedrooms'].replace('Pièce(s)', '').strip()
            del item['bedrooms']
        elif 'Appart' in item['bedrooms']:
            del item['bedrooms']
        else:
            item['bedrooms'] = item['bedrooms'].replace('S', '').replace('+', '').replace('Chambre', '').replace('s',
                                                                                                                 '').strip()
    if exists('rooms', item):
        try:
            item['rooms'] = round(float(item['rooms'].replace(' ','').strip()))
            if item['rooms'] not in range(0,50):
                del item['rooms']
        except:
            del item['rooms']
    if exists('bedrooms', item):
        try:
            item['bedrooms'] = round(float(item['bedrooms'].replace(' ','').replace('et', '').replace('e','').strip()))
            if item['bedrooms'] not in range(0,50):
                del item['bedrooms']
        except:
            del item['bedrooms']
    if exists('bathrooms', item):
        if str(item['bathrooms']).replace(' ','') != '':
            item['bathrooms'] = round(float(str(item['bathrooms']).replace('Salles de bains', '').replace('Salle de bain','').replace('Salle(s)','').replace('+','')))

        else:
            del item['bathrooms']
    if exists('parking', item):
        if item['parking'] != 'Non':
            item['parking'] = 'Yes'
        else:
            item['parking'] = 'No'
    if exists('heating', item):
        item['heating'] = 'Yes'
    if exists('floor', item):
        try:
            item['floor'] = round(float(str(item['floor']).replace('ème', '')\
                .replace('Appartement au rez-de-chaussée','0').replace('(étage moyen)','')\
                .replace('(étage elevé)', '').replace('(étage dernier)','').replace('(étage bas)', '').replace('Terre', '0')\
                .replace('er','').replace('+','').replace(' ','').replace('(étage terre)', '').strip()))
        except Exception as e:
            del item['floor']
    if exists('garage', item):
        item['garage'] = 'Yes'
    if exists('air_conditioning', item):
        item['air_conditioning'] = 'Yes'
    if exists('elevator', item):
        if item['elevator'] == 'Non':
            item['elevator'] = 'No'
        else:
            item['elevator'] = 'Yes'
    if exists('balcony', item):
        item['balcony'] = 'Yes'
    if exists('equipped_kitchen', item):
        item['equipped_kitchen'] = 'Yes'
    '''
for d_item in to_del:
    while d_item in data:
        data.remove(d_item)
print(f"Changed {counter} records.")
details = {}
for item in data:
    for key in item:
        if item[key] != "N/A":
            if key in details.keys():
                details[key] += 1
            else:
                details[key] = 1
        elif key not in details.keys():
            details[key] = 0

details = {key: value for key, value in sorted(details.items(), key=lambda item: item[1], reverse=True)}
total = len(data)
print(f"Total records: {total}")
print(f"Total columns unfiltered {len(details)}")
print("-----------DETAILS-----------")
for detail in details.keys():
    if round(details[detail] / total * 100, 2) > 10:
        print(f"Detail : {detail}, {round(details[detail] / total * 100, 2)}%|{details[detail]}")
print("-----------MORE DETAILS-----------")
removed_details = [x for x in details if round(details[x] / total * 100, 2) < 10]
for item in data:
    for removed_detail in removed_details:
        if removed_detail in item.keys():
            del item[removed_detail]
print("Number of columns left:", len(details) - len(removed_details))

'''for item in data:
    if not exists('bedrooms', item) and exists('description', item):
        print(item['description'])
        pass'''

'''for item in data:
    if not exists('floor', item) and exists('description',item):
        match = re.search(r"^.{1,10}etage.{1,10}$", item['description'].lower())
        print(match)
        if match:
            print(match.group())
        #print(item['description'])'''

for item in data:
    for key in list(item.keys()):
        if item[key] == 'N/A':
            del item[key]

''''''
with open(f'../../data/PreProcessed/Treated.json', 'w', encoding="utf-8") as file:
    json.dump(data, file, indent=4, ensure_ascii=False)
