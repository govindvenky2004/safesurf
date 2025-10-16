import requests
import json

API_KEY = "AIzaSyCytvF0mIdAT_dPHTlKjHIXpWAPummbeCI"
url = "https://allegro.53489715.xyz/robot-check"  # Replace with the URL you want to check

headers = {
    "Content-Type": "application/json"
}

payload = {
    "client": {
        "clientId": "your-client-id",  # Replace with your client ID
        "clientVersion": "1.0.0"       # Replace with your client version
    },
    "threatInfo": {
        "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE"],  # Valid threat types
        "platformTypes": ["ANY_PLATFORM"],
        "threatEntryTypes": ["URL"],
        "threatEntries": [
            {"url": url}
        ]
    }
}


response = requests.post(
    f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={API_KEY}",
    headers=headers,
    data=json.dumps(payload)
)

result = response.json()

if result:
    print("Threat found:", result)
else:
    print("No threats detected for the URL.")
