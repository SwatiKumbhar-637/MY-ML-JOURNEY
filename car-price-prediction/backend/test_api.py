import requests

url = "http://127.0.0.1:5000/predict"

data = {
    "company": "Maruti",
    "fuel_type": "Petrol",
    "car_age": 5,
    "kms_driven": 45000,
    "model": "random_forest"
}

response = requests.post(url, json=data)

print(response.json())