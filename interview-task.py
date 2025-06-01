import requests
import json

project_id = 'rn-firebase-ml-test'
collection_name = 'patientData'

url = f'https://firestore.googleapis.com/v1/projects/rn-firebase-ml-test/databases/(default)/documents/patientData'

# function to fetch data from firestore
def fetch_data():
    try:
        #get request
        response = requests.get(url)

        #if successful
        if response.status_code == 200:
            data = response.json()

            #print data
            for doc in data['documents']:
                print(json.dumps(doc, indent=4)) # pretty print the documents data
            else:
                print(f"Error: {response.status_code}")
                print(response.text)
    except Exception as e:
        print(f"Error: {e}")

# call the function
fetch_data()