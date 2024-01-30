import json
import requests
# Constants
BASE_URL = "https://api-eu.libreview.io"
HEADERS = {
    'accept-encoding': 'gzip',
    'cache-control': 'no-cache',
    'connection': 'Keep-Alive',
    'content-type': 'application/json',
    'product': 'llu.android',
    'version': '4.7'
}

# Function to log in and retrieve JWT token
def login(email, password):
    endpoint = "/llu/auth/login"
    payload = {
        "email": email,
        "password": password
    }
    
    response = requests.post(BASE_URL + endpoint, headers=HEADERS, json=payload)
    response.raise_for_status()
    data = response.json()
    token = data.get('data', []).get("authTicket", []).get("token", []) 
    return token

# Function to get connections of patients
def get_patient_connections(token):
    endpoint = "/llu/connections" 
    headers = {**HEADERS, 'Authorization': f"Bearer {token}"}
    
    response = requests.get(BASE_URL + endpoint, headers=headers)
    response.raise_for_status()
    return response.json()

# Function to retrieve CGM data for a specific patient
def get_cgm_data(token, patient_id):
    endpoint = f"/llu/connections/{patient_id}/graph"  
    headers = {**HEADERS, 'Authorization': f"Bearer {token}"}
    
    response = requests.get(BASE_URL + endpoint, headers=headers)
    response.raise_for_status()
    return response.json()

# Main Function
def glucose_value():
    email = ""  # Replace with your actual email
    password = ""   # Replace with your actual password

    token = login(email, password)
    patient_data = get_patient_connections(token)
    
    patient_id = patient_data['data'][0]["patientId"]
    cgm_data = get_cgm_data(token, patient_id)
    
    #Take the last glucose value
    last_glucose = cgm_data['data']['graphData'][-1]['Value']
    previous_glucose = cgm_data['data']['graphData'][-2]['Value']
    return last_glucose, previous_glucose
