import json
from fuzzywuzzy import fuzz

json_file_path = '../../data/processed/processed.json'
output_file_path = '../../data/processed/processed.json'


def remove_redundant_records(json_file, output_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Filter out records that do not have 'price' or 'surface'
    records = [record for record in data if 'price' in record and 'surface' in record]

    unique_records = []
    seen = set()

    for record in records:
        identifier = (record['price'], record['surface'])
        is_redundant = False

        for unique_record in unique_records:
            if identifier == (unique_record['price'], unique_record['surface']):
                if 'description' in record and 'description' in unique_record:
                    if fuzz.token_sort_ratio(record['description'], unique_record['description']) > 90:
                        is_redundant = True
                        print(f"Record matches with same price, surface, and description similarity > 90%")
                        break

        if not is_redundant:
            unique_records.append(record)

    # Save the cleaned data
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(unique_records, f, ensure_ascii=False, indent=4)

    print(f"Original records: {len(records)}")
    print(f"Unique records after removing redundancy: {len(unique_records)}")
    print(f"Cleaned data saved to {output_file}")


# Example usage
remove_redundant_records(json_file_path, output_file_path)