import json
import re
import os

# Function to extract neighboring words around a keyword in a text


def extract_neighboring_words(text, keyword, window=3):
    words = text.split()
    # Find all occurrences of the keyword in the text
    matches = [i for i, word in enumerate(words) if keyword in word.lower()]

    extracted_phrases = []
    for index in matches:
        # Define the range of neighboring words to extract
        start = max(0, index - window)
        end = min(len(words), index + window + 1)
        extracted_phrases.append(" ".join(words[start:end]))

    return extracted_phrases


def replace_accents(text):
    return text.replace("é", "e").replace("è", "e")

def extract_floor_number(description):
    # Define regex patterns to match different formats of floor descriptions in French
    floor_patterns = [
        # Matches "1er étage", "2ème étage", etc.
        r"\b(\d+)\s?-?\s?(?:er|e|eme)\s?(?:etage|tage|etg|etages)\b",
        # Matches "étage 1", "étage 2", etc.
        r"\b(?:etage)\s?(\d+)\b",
        # Matches "rez-de-chaussée", "rdc"
        r"\b(?:\w*rez[-\s]?de[-\s]?chaus\w*|rdc)\b",
        # Matches "premier étage"
        r"\bpremi(?:er|ere)\s?(?:etage|tage|etg|etages)\b",
        # Matches "deuxième étage"
        r"\bdeuxieme\s?(?:etage|tage|etg|etages)\b",
        # Matches "troisième étage"
        r"\btroisieme\s?(?:etage|tage|etg|etages)\b",
        # Matches "quatrième étage"
        r"\bquatrieme\s?(?:etage|tage|etg|etages)\b",
        # Matches "cinquième étage"
        r"\bcinquieme\s?(?:etage|tage|etg|etages)\b",
        # Matches "sixième étage"
        r"\bsixieme\s?(?:etage|tage|etg|etages)\b",
        # Matches "septième étage"
        r"\bseptieme\s?(?:etage|tage|etg|etages)\b",
        # Matches "huitième étage"
        r"\bhuitieme\s?(?:etage|tage|etg|etages)\b",
        # Matches "neuvième étage"
        r"\bneuvieme\s?(?:etage|tage|etg|etages)\b",
        # Matches "dixième étage"
        r"\bdixieme\s?(?:etage|tage|etg|etages)\b"
    ]

    for pattern in floor_patterns:
        match = re.search(pattern, description, re.IGNORECASE)

        if match:
            if "rez" in match.group(0).lower() or "rdc" in match.group(0).lower():
                return 0  # Return 0 for "rez-de-chaussée" or "rdc"
            if "premier" in match.group(0).lower() or "premiere" in match.group(0).lower() or "1" in match.group(0).lower():
                return 1  # Return 1 for "premier étage"
            if "deuxieme" in match.group(0).lower() or "2" in match.group(0).lower():
                return 2  # Return 2 for "deuxième étage"
            if "troisieme" in match.group(0).lower() or "3" in match.group(0).lower():
                return 3  # Return 3 for "troisième étage"
            if "quatrieme" in match.group(0).lower() or "4" in match.group(0).lower():
                return 4  # Return 4 for "quatrième étage"
            if "cinquieme" in match.group(0).lower() or "5" in match.group(0).lower():
                return 5  # Return 5 for "cinquième étage"
            if "sixieme" in match.group(0).lower() or "6" in match.group(0).lower():
                return 6  # Return 6 for "sixième étage"
            if "septieme" in match.group(0).lower() or "7" in match.group(0).lower():
                return 7  # Return 7 for "septième étage"
            if "huitieme" in match.group(0).lower() or "8" in match.group(0).lower():
                return 8  # Return 8 for "huitième étage"
            if "neuvieme" in match.group(0).lower() or "9" in match.group(0).lower():
                return 9  # Return 9 for "neuvième étage"
            if "dixieme" in match.group(0).lower() or "10" in match.group(0).lower():
                return 10  # Return 10 for "dixième étage"
            return int(match.group(1))  # Return the matched floor number
    return None  # Return None if no match is found

# Function to process the dataset and check for the presence of an elevator


def process_dataset(file_path, output_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    total_records = len(json_data)
    floor_records = 0

    for record in json_data:
        # If "elevator" key is missing, check the description for mentions of "ascenseur"
        if "elevator" not in record:
            description = record.get("description", "").lower()
            elevator_mentions = extract_neighboring_words(
                description, "ascenseur")

            # Add a new field "elevator_check" with extracted mentions or mark as "No"
            if elevator_mentions:
                # Join list into a single string
                elevator_mentions_str = ' '.join(elevator_mentions)

                # record["elevator_check"] = elevator_mentions
                if re.search(r'avec\s+.*\bascenseur(s)?\b', elevator_mentions_str, re.IGNORECASE) or \
                        re.search(r'(double|deux|un|2)\s+ascenseur(s)?\b', elevator_mentions_str, re.IGNORECASE) or \
                        re.search(r"ascenseur\s*:\s*oui\b", elevator_mentions_str, re.IGNORECASE) or \
                        re.search(r'accès\s+ascenseur\b', elevator_mentions_str, re.IGNORECASE) or \
                        re.search(r"ascenseur\s*:\s*ascenseur\b", elevator_mentions_str, re.IGNORECASE) or \
                        re.search(r"munie\s+d\s+.*\bascenseur(s)?\b", elevator_mentions_str, re.IGNORECASE):
                    record["elevator"] = "Yes"
                elif re.search(r'sans\s+ascenseur(s)?\b', elevator_mentions_str, re.IGNORECASE) or \
                        re.search(r"pas\s+d’ascenseur\b", elevator_mentions_str, re.IGNORECASE) or \
                        re.search(r"pas\s+d\'ascenseur\b", elevator_mentions_str, re.IGNORECASE) or \
                        re.search(r"ascenseur\s*:\s*non\b", elevator_mentions_str, re.IGNORECASE) or \
                        re.search(r"absence\s+d\'ascenseur\b", elevator_mentions_str, re.IGNORECASE) or \
                        re.search(r'ascenseur\s+en\s+panne\b', elevator_mentions_str, re.IGNORECASE) or \
                        re.search(r'ss\s+ascenseur\b', elevator_mentions_str, re.IGNORECASE) or \
                        re.search(r'sauf\s+ascenseur\b', elevator_mentions_str, re.IGNORECASE):
                    record["elevator"] = "No"
                else:
                    record["elevator"] = "Yes"

            else:
                record["elevator"] = "No"
            # record["elevator_check"] = elevator_mentions if elevator_mentions else "No"

        if "floor" not in record:
            description = record.get("description", "").lower()
            description = replace_accents(description)
            floor_keywords = r"etage|tage|etg|\w*rez[-\s]?de[-\s]?chaus\w*|rdc"
            floor_mentions = []

            for match in re.finditer(floor_keywords, description):
                floor_mentions.extend(extract_neighboring_words(
                    description, match.group(), window=3))

            # Count occurrences of "étage" and "rez de chausse" within the record
            etage_count = len(re.findall(
                r"etage|tage|etg|etages", description))
            rez_de_chaussee_count = len(re.findall(
                r"\w*rez[-\s]?de[-\s]?chaus\w*|rdc", description))

            # Store the counts in the record
            record["etage_count"] = etage_count
            record["rez_de_chaussee_count"] = rez_de_chaussee_count

            # if etage_count == 0 and rez_de_chaussee_count == 0:
            #     record["floor"] = None

            # Add a new field "floor_check" with extracted mentions or mark as "No"
            if floor_mentions:
                record["floor_description"] = ' '.join(floor_mentions)
                floor_number = extract_floor_number(
                    record["floor_description"])
                if floor_number is not None:
                    record["floor"] = floor_number

        if "floor" in record:
            floor_records += 1

    floor_percentage = (floor_records / total_records) * 100

    print(f"Total records: {total_records}")
    print(f"Records with floor information: {floor_records}")
    print(
        f"Percentage of records with floor information: {floor_percentage:.2f}%")

    # Save the processed data back to a JSON file
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(json_data, file, indent=4, ensure_ascii=False)


# Example usage: specify input and output file paths
input_file = os.path.join(os.path.dirname(
    __file__), "../../data/PreProcessed/Treated.json")
output_file = os.path.join(os.path.dirname(
    __file__), "../../data/PreProcessed/Treated.json")
# input_file = '/src/data/copy.json'
# output_file = '/src/data/processed_dataset.json'
process_dataset(input_file, output_file)


# def count_records_without_description(json_file):
#     with open(json_file, 'r', encoding='utf-8') as f:
#         data = json.load(f)
#     print(len(data))
#     count = 0
#     for record in data:
#         if 'floor' not in record:
#             count += 1
#             # if count < 100:
#             print(record)
#     print(count)
#     print((count/len(data))*100)
#     return count


# json_file_path = os.path.join(os.path.dirname(
#     __file__), "../../data/PreProcessed/Treated.json")
# count = count_records_without_description(json_file_path)
