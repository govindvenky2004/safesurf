import imaplib
import email
import logging
import joblib
import re
from flask import Flask, jsonify, request
from flask_cors import CORS
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords
import string
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import socket
import ssl
import whois
from urllib.parse import urlparse
from pymongo import MongoClient
import string

from bson import ObjectId
# Ensure NLTK stopwords are downloaded
nltk.download('stopwords')

app = Flask(__name__)
CORS(app)

# MongoDB Configuration
client = MongoClient('mongodb://localhost:27017/')  # Update with your MongoDB URI if necessary
db = client['SAFESURFDB']  # Replace with your database name
url_collection = db['url'] 
email_collection=db['email'] # Replace with your collection name

GOOGLE_API_KEY = 'AIzaSyCytvF0mIdAT_dPHTlKjHIXpWAPummbeCI'  # Replace with your actual Google API key
SAFE_BROWSING_URL = 'https://safe-browsing.googleapis.com/v4/threatMatches:find?key=' + GOOGLE_API_KEY

# Logger Configuration
logging.basicConfig(level=logging.WARNING)
# Load pre-trained models
model = joblib.load('naive_bayes_model.pkl')  # Email classification model
url_model = joblib.load('random_forest_model.pkl')  # URL classification model

# Load pre-trained TF-IDF vectorizer
tfidf_vectorizer = joblib.load('tfidf_vectorizer.pkl')  # TF-IDF vectorizer

def get_body_from_email(msg):
    """Extract the body of the email"""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                return part.get_payload(decode=True).decode()
    else:
        return msg.get_payload(decode=True).decode()

@app.route('/analyze_email', methods=['POST'])
def analyze_email():
    # Get email address, password, and folder from the request body
    email_address = request.json.get('email')
    email_password = request.json.get('password')
    folder = request.json.get('folder', 'inbox').lower()

    if not email_address or not email_password:
        return jsonify({'error': 'Email and password are required'}), 400

    # Adjust folder validation for Gmail
    if folder not in ['inbox', 'spam']:
        return jsonify({'error': 'Invalid folder name. Please choose "inbox" or "spam".'}), 400

    if folder == 'spam':  # Handling Gmail's spam folder
        folder = '[Gmail]/Spam'

    try:
        # Connect to the email server
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(email_address, email_password)

        # Select the folder
        mail.select(folder)
        status, messages = mail.search(None, 'UNSEEN')
        email_ids = messages[0].split()

        # List to store the analysis results
        analyzed_emails = []

        for e_id in email_ids:
            # Fetch the email
            status, data = mail.fetch(e_id, '(RFC822)')

            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])

                    # Extract subject and body
                    subject = msg.get('Subject', 'No Subject')
                    body = get_body_from_email(msg)

                    # Combine subject and body for prediction
                    text_data = f"{subject} {body}"

                    # Preprocess text and transform it to TF-IDF features
                    tfidf_features = tfidf_vectorizer.transform([text_data])

                    # Make email prediction (phishing or legitimate)
                    email_prediction = model.predict(tfidf_features)

                    # Interpret the email prediction
                    if email_prediction == 1:
                        prediction_label = 'phishing'
                        message = "This email looks suspicious and might be a phishing attempt."
                    else:
                        prediction_label = 'legitimate'
                        message = "This email looks safe and is legitimate."

                    # Store the analysis result in MongoDB
                    email_data = {
                        'subject': subject,
                        'sender': msg.get('From', ''),
                        'body': body,
                        'prediction': prediction_label,
                        'message': message,
                        'folder': folder,
                        'timestamp': msg.get('Date', ''),
                        'email_address': email_address
                    }

                    # Insert result into the MongoDB collection
                    insert_result = email_collection.insert_one(email_data)
                    logging.info(f"Email data inserted with ID: {insert_result.inserted_id}")


                    # Add to analyzed emails list
                    analyzed_emails.append(email_data)

        # Logout from the email server
        mail.logout()

        # Return the results
        return jsonify({
            'message': f'Analyzed unread emails from the {folder} folder successfully.',
            'analyzed_emails': analyzed_emails
        }), 200

    except imaplib.IMAP4.error as e:
        logging.error(f"Error accessing the email server: {e}")
        return jsonify({'error': 'Failed to access the email server.'}), 500

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return jsonify({'error': 'An unexpected error occurred.'}), 500




@app.route('/get_email_results', methods=['GET'])
def get_email_results():
    try:
        # Fetch the latest email results from the MongoDB collection by sorting on timestamp
        email_results = list(email_collection.find().sort('timestamp', -1))  # Sort by 'timestamp' in descending order

        # Convert the ObjectId to string for JSON serialization
        for email in email_results:
            email['_id'] = str(email['_id'])  # Convert ObjectId to string

        # Check if results are found
        if not email_results:
            return jsonify({'message': 'No email results found.'}), 404

        # Return the results as a JSON response
        return jsonify({
            'message': 'Successfully fetched email results.',
            'email_results': email_results
        }), 200

    except Exception as e:
        logging.error(f"Error fetching email results: {e}")
        return jsonify({'error': 'An unexpected error occurred while fetching the results.'}), 500


# Load the feature transformer if you use one
# transformer = joblib.load('path_to_your_feature_transformer.pkl') # If you use one

# Function to extract features from a URL (make sure it matches the features used for training)
def safe_get(url, timeout=10):
    try:
        response = requests.get(url, verify=False, timeout=timeout)
        return response
    except requests.exceptions.Timeout:
        print(f"Timeout occurred while trying to access: {url}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
    return None  # In case of error, return None

# Function to get the WHOIS information for a domain
def get_whois_info(domain):
    try:
        w = whois.whois(domain)
        creation_date = w.creation_date
        # Handle cases where creation_date is returned as a list or a single value
        if isinstance(creation_date, list):
            return creation_date[0] if creation_date else None
        return creation_date
    except Exception as e:
        print(f"Error fetching WHOIS info for {domain}: {e}")
        return None

# Function to check SSL certificate details
def check_ssl_certificate(domain):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                return cert is not None
    except Exception as e:
        print(f"Error checking SSL certificate for {domain}: {e}")
        return False

# Function to extract features from a URL based on the given attributes
def extract_features(url):
    features = {}

    # Step 1: Validate URL format
    try:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        if not domain:
            print(f"Invalid URL: {url}")
            return None
    except Exception as e:
        print(f"Error parsing URL {url}: {e}")
        return None

    # Step 2: Extract features
    try:
        features['having_IP_Address'] = 1 if bool(re.search(r'\d+\.\d+\.\d+\.\d+', url)) else -1
        features['URL_Length'] = 1 if len(url) < 54 else (0 if len(url) <= 75 else -1)
        features['Shortining_Service'] = 1 if any(service in url for service in ["bit.ly", "goo.gl", "tinyurl.com", "is.gd", "t.co", "ow.ly"]) else -1
        features['having_At_Symbol'] = 1 if '@' in url else -1
        features['double_slash_redirecting'] = 1 if '//' in url else -1
        features['Prefix_Suffix'] = 1 if url.startswith('www.') or url.endswith('.com') else -1
        features['having_Sub_Domain'] = 1 if len(parsed_url.netloc.split('.')) > 2 else 0
        features['SSLfinal_State'] = 1 if url.startswith('https') else (0 if 'https' not in url else -1)
    except Exception as e:
        print(f"Error extracting basic URL features for {url}: {e}")
        return None

    # Step 3: Fetch WHOIS data
    domain_creation_date = get_whois_info(domain)
    if domain_creation_date:
        current_year = datetime.now().year
        domain_creation_year = domain_creation_date.year if isinstance(domain_creation_date, datetime) else None
        if domain_creation_year:
            features['Domain_registeration_length'] = 1 if (current_year - domain_creation_year > 2) else -1
        else:
            features['Domain_registeration_length'] = -1
    else:
        features['Domain_registeration_length'] = -1

    # Step 4: Fetch page content using safe_get
    page = safe_get(url, timeout=10)  # Increased timeout to 10 seconds
    if page is None:
        print(f"Failed to fetch page content for {url}")
        return None  # If page fetch fails, return None

    # Step 5: Parse the HTML content
    try:
        soup = BeautifulSoup(page.text, 'html.parser')

        # Feature extraction from page content
        features['Favicon'] = 1 if soup.find('link', rel='icon') else -1
        features['port'] = 1 if ':' in parsed_url.netloc else -1
        features['HTTPS_token'] = 1 if 'https' in parsed_url.scheme else -1
        features['Request_URL'] = 1 if domain in str(soup.find_all('a')) else -1
        features['URL_of_Anchor'] = 1 if any(anchor.get('href') for anchor in soup.find_all('a')) else 0
        features['Links_in_tags'] = 1 if soup.find_all('a') else (0 if not soup.find_all('a') else 0)
        features['SFH'] = 1 if soup.find('form') else (0 if not soup.find('form') else 0)
        features['Submitting_to_email'] = 1 if 'mailto:' in str(soup.find_all('a')) else 0
        features['Abnormal_URL'] = 1 if bool(re.search(r'[^a-zA-Z0-9.-]', url)) else 0
        features['Redirect'] = 1 if any(meta.get('http-equiv') == 'refresh' for meta in soup.find_all('meta')) else 0
        features['on_mouseover'] = 1 if any('onmouseover' in str(tag.attrs) for tag in soup.find_all()) else 0
        features['RightClick'] = 1 if any('contextmenu' in str(tag.attrs) for tag in soup.find_all()) else 0
        features['popUpWidnow'] = 1 if any('popup' in str(tag.attrs) for tag in soup.find_all()) else 0
        features['Iframe'] = 1 if any('iframe' in str(tag.attrs) for tag in soup.find_all()) else 0

        # Suspicious keywords in page content
        # Check for robots.txt presence
        
    except Exception as e:
        print(f"Error parsing page content for {url}: {e}")
        return None

    # Step 6: Additional features (placeholders)
    features['age_of_domain'] = 1 if domain_creation_date else 0
    features['DNSRecord'] = 1 if bool(parsed_url.netloc) else 0
    features['web_traffic'] = 1  # Placeholder
    features['Page_Rank'] = 1    # Placeholder
    features['Google_Index'] = 1  # Placeholder
    features['Links_pointing_to_page'] = 1  # Placeholder
    features['Statistical_report'] = 1  # Placeholder

    return features

# Example usage
"""url = "http://google.com"
features = extract_features(url)
if features:
    print(features)
else:
    print("Feature extraction failed.")"""


# Function to analyze the URL using the trained model
def analyze_url_with_google_api(url):
    """
    Check URL with Google Safe Browsing API.
    """
    payload = {
        "client": {
            "clientId": "your_client_id",  # Replace with your client ID if needed
            "clientVersion": "1.0"
        },
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "POTENTIALLY_HARMFUL_APPLICATION"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}]
        }
    }

    try:
        response = requests.post(SAFE_BROWSING_URL, json=payload)
        data = response.json()

        if 'matches' in data:
            # If there are matches, the URL is considered unsafe
            return "Suspicious"
        else:
            # No matches, the URL is safe according to Google Safe Browsing
            return "Safe"

    except Exception as e:
        return f"Error checking URL with Google API: {str(e)}"

# Assuming you already have a trained model and Google Safe Browsing API function
# If not, the actual functionality should be implemented here (e.g., extract_features, url_model, analyze_url_with_google_api)


# MongoDB setup (make sure your MongoDB client and collection are defined)
# Example: collection = db.get_collection('url_analysis')

def analyze_url(url):
    # Extract features from the URL
    features = extract_features(url)
    features = list(features.values())

    # Predict with the trained model
    prediction = url_model.predict([features])[0]

    # Analyze URL with Google Safe Browsing API
    google_analysis = analyze_url_with_google_api(url)

    # Combine the model prediction and Google API result
    if prediction == 1:  # If model detects phishing
        model_result = "Suspicious"
    else:  # If model detects legitimate
        model_result = "Safe"

    # Decision logic to combine both results:
    # If either the model or Google API marks the URL as suspicious, it will be flagged as suspicious.
    if google_analysis == "Suspicious" or model_result == "Suspicious":
        final_prediction = "Suspicious"
    else:
        final_prediction = "Safe"

    return {"final_prediction": final_prediction}

@app.route('/analyze_url', methods=['POST'])
def analyze_url_route():
    # Get the URL from the request body
    url = request.json.get('url')

    if not url:
        return jsonify({'error': 'URL is required'}), 400

    # Analyze the URL using the analyze_url function
    try:
        analysis_result = analyze_url(url)
    except Exception as e:
        logging.error(f"Error analyzing URL '{url}': {e}")
        return jsonify({'error': 'Failed to analyze URL'}), 500

    # Prepare data to store in MongoDB
    result_data = {
        "url": url,
        "prediction": analysis_result,
        "timestamp": datetime.utcnow().isoformat()
    }

    try:
        # Insert the result into MongoDB
        result = url_collection.insert_one(result_data)
        logging.info(f"Result for URL '{url}' saved to database.")
        
        # Convert ObjectId to string for JSON serialization
        result_data["_id"] = str(result.inserted_id)
    except Exception as e:
        logging.error(f"Error saving result for URL '{url}': {e}")
        return jsonify({'error': 'Failed to save result'}), 500

    # Return the analysis result as a response
    return jsonify({
        'message': 'URL analyzed and saved successfully.',
        'result': result_data
    }), 201
@app.route('/get_url_results', methods=['GET'])
def get_url_results():
    # Get the URL from the request query parameter
    url = request.args.get('url')
    
    # Debugging: Log the incoming request URL
    app.logger.info(f'Received request with URL parameter: {url}')
    
    if not url:
        app.logger.error('No URL parameter provided')
        return jsonify({'error': 'URL parameter is required'}), 400

    try:
        # Check if the URL exists in the database
        result = url_collection.find_one({"url": url})
        
        if result:
            # If result exists in the database, return it
            prediction = result['prediction']  # Assuming the prediction field exists
            timestamp = result['timestamp']  # Assuming the timestamp field exists
        else:
            # If the URL is not in the database, perform the analysis (dummy for now)
            prediction = "Safe"  # Simulate the prediction (replace with real analysis)
            timestamp = datetime.now().isoformat()

            # Insert the result into the database (optional)
            url_collection.insert_one({
                "url": url,
                "prediction": prediction,
                "timestamp": timestamp
            })

        # Prepare the response data
        response_data = {
            "url": url,
            "prediction": prediction,
            "timestamp": timestamp
        }

        app.logger.info(f'Generated analysis result for URL: {url}')
        return jsonify(response_data), 200

    except Exception as e:
        app.logger.error(f'Error generating analysis: {e}')
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)

