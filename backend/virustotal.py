import requests

def check_url_with_virustotal(api_key, url):
    # VirusTotal API endpoint
    endpoint = "https://www.virustotal.com/api/v3/urls"
    
    # Encode the URL in base64 format as required by VirusTotal
    import base64
    encoded_url = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
    
    # Make the request to the VirusTotal API
    headers = {
        "x-apikey": api_key
    }
    response = requests.get(f"{endpoint}/{encoded_url}", headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Error {response.status_code}: {response.text}"}

# Example usage
api_key = "0e6c55d797a5536ed2e09726f583887b90eb3f2086bfbc0280380074811c75d7"
url_to_check = "http://tonkeepere.com"
result = check_url_with_virustotal(api_key, url_to_check)
print(result)
