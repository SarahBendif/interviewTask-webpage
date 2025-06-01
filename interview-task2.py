import requests
import json

project_id = 'rn-firebase-ml-test'
collection_name = 'patientData'

url = f'https://firestore.googleapis.com/v1/projects/rn-firebase-ml-test/databases/(default)/documents/patientData'

# function to convert data values
def parse_firestore_value(value):
    """handles firestore's typed values"""
    if 'integerValue' in value:
        return int(value['integerValue'])
    elif 'doubleValue' in value:
        return float(value['doubleValue'])
    elif 'stringValue' in value:
        return value['stringValue']
    elif 'arrayValue' in value:
        return [parse_firestore_value(v) for v in value['arrayValue'].get('values', [])]
    elif 'mapValue' in value:
        return parse_firestore_value(value['mapValue']['fields'])
    return value

def parse_firestore_map(fields):
    return {k: parse_firestore_value(v) for k, v in fields.items()}

def fetch_and_save():
    res = requests.get(url)
    if res.status_code != 200:
        print(f"Error: {res.status_code}")
        return

    raw_docs = res.json().get("documents", [])
    parsed_docs = []

    for doc in raw_docs:
        fields = doc.get("fields", {})
        data = {
            "id": doc["name"].split("/")[-1],
            "date": parse_firestore_value(fields.get("date", {})),
            "activity": parse_firestore_map(fields.get("activity", {}).get("mapValue", {}).get("fields", {})),
            "nutrition": parse_firestore_map(fields.get("nutrition", {}).get("mapValue", {}).get("fields", {})),
            "sleep": parse_firestore_map(fields.get("sleep", {}).get("mapValue", {}).get("fields", {})),
            "vitals": parse_firestore_map(fields.get("vitals", {}).get("mapValue", {}).get("fields", {})),
        }
        parsed_docs.append(data)

    with open("patient_data.json", "w") as f:
        json.dump(parsed_docs, f, indent=2)

    print("✅ Data written to patient_data.json")

fetch_and_save()