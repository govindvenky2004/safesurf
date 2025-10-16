import pymongo
import joblib
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests
import pandas as pd

# MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB URI
db = client["url"]  # Replace with your database name
collection = db["url"]  # Replace with your collection name

# Load the pre-trained RandomForest model
model = joblib.load('random_forest_model.pkl')  # Replace with the actual path to your saved model

def extract_features_from_url(url):
    """
    Extract features from a given URL for phishing detection.

    Parameters:
        url (str): The URL to analyze.

    Returns:
        dict: A dictionary of extracted features.
    """
    # Try fetching the page content for feature extraction
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise HTTPError for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return {}  # Return empty features if the URL cannot be fetched

    # Extract features based on the URL structure and content
    features = {
        'having_IP_Address': 1 if bool(re.search(r'\d+\.\d+\.\d+\.\d+', url)) else -1,
        'URL_Length': len(url),
        'Shortining_Service': 1 if any(shortener in url for shortener in ["bit.ly", "goo.gl", "tinyurl"]) else -1,
        'having_At_Symbol': 1 if '@' in url else -1,
        'double_slash_redirecting': 1 if '//' in url[7:] else -1,  # Exclude protocol
        'Prefix_Suffix': 1 if '-' in urlparse(url).netloc else -1,
        'having_Sub_Domain': 1 if len(urlparse(url).netloc.split('.')) > 2 else -1,
        'SSLfinal_State': 1 if url.startswith('https') else -1,
        'Domain_registeration_length': 1 if len(urlparse(url).netloc.split('.')) == 2 else -1,
        'Favicon': 1 if soup.find('link', rel='icon') else -1,
        'port': 1 if urlparse(url).port else -1,
        'HTTPS_token': 1 if 'https' in url else -1,
        'Request_URL': 1 if urlparse(url).netloc in str(soup.find_all('a')) else -1,
        'URL_of_Anchor': 1 if any(anchor.get('href') for anchor in soup.find_all('a')) else -1,
        'Links_in_tags': 1 if soup.find_all(['a', 'link', 'script']) else -1,
        'SFH': 1 if soup.find('form') else -1,
        'Submitting_to_email': 1 if 'mailto:' in str(soup.find_all('a')) else -1,
        'Abnormal_URL': 1 if re.search(r'\d{4,}', url) else -1,
        'Redirect': 1 if any(meta.get('http-equiv') == 'refresh' for meta in soup.find_all('meta')) else -1,
        'on_mouseover': 1 if any('onmouseover' in str(tag.attrs) for tag in soup.find_all()) else -1,
        'RightClick': 1 if any('contextmenu' in str(tag.attrs) for tag in soup.find_all()) else -1,
        'popUpWidnow': 1 if any('popup' in str(tag.attrs) for tag in soup.find_all()) else -1,
        'Iframe': 1 if soup.find('iframe') else -1,
        'age_of_domain': -1,  # Placeholder (can be populated with WHOIS data)
        'DNSRecord': 1 if bool(urlparse(url).netloc) else -1,
        'web_traffic': -1,  # Placeholder (can use Alexa rank API or similar)
        'Page_Rank': -1,  # Placeholder (can use external ranking data)
        'Google_Index': 1 if 'Googlebot' in str(soup) else -1,
        'Links_pointing_to_page': len(soup.find_all('a')),
        'Statistical_report': -1,  # Placeholder (statistical data if available)
    }

    return features

# Retrieve all documents (URLs) from MongoDB collection
urls_cursor = collection.find({}, {"url": 1})  # Only fetch URLs

# List to store feature dictionaries
feature_list = []
urls = []

# Process each URL and extract features
for document in urls_cursor:
    url = document.get('url', '')
    if url:
        features = extract_features_from_url(url)
        if features:  # Ensure valid features are returned
            feature_list.append(features)
            urls.append(url)

# Convert feature list to a DataFrame for model prediction
if feature_list:
    df = pd.DataFrame(feature_list)

    # Ensure the DataFrame matches the model's expected features
    if not df.empty:
        try:
            # Make predictions using the RandomForest model
            predictions = model.predict(df)

            # Update predictions back into MongoDB
            for url, prediction in zip(urls, predictions):
                collection.update_one({"url": url}, {"$set": {"prediction": int(prediction)}})

            print("Predictions completed and stored in MongoDB.")
        except Exception as e:
            print(f"Error during prediction: {e}")
    else:
        print("Feature extraction returned an empty DataFrame.")
else:
    print("No URLs found or valid features to process.")
