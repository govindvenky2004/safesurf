import joblib
import pandas as pd
from url_features import extract_url_features  # Ensure this import is correct
from db_manager import get_urls_from_db  # Function to get the training URLs, replace with your own method
import urllib3
from requests.exceptions import SSLError, ConnectionError, Timeout

# Disable SSL warnings (Optional: Useful during testing, but avoid in production)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Function to extract features with SSL error handling
def safe_extract_url_features(url):
    try:
        return extract_url_features(url)
    except SSLError as e:
        print(f"SSL error for URL {url}: {e}")
    except ConnectionError as e:
        print(f"Connection error for URL {url}: {e}")
    except Timeout as e:
        print(f"Timeout error for URL {url}: {e}")
    except Exception as e:
        print(f"Unexpected error for URL {url}: {e}")
    return None

# Fetch URLs from the database
print("Fetching URLs from the database...")
data = get_urls_from_db()  # Replace this with the correct method to fetch the training URLs
print(f"Fetched {len(data)} URLs for feature extraction.")

# Extract features for each URL
feature_list = []
for record in data:
    try:
        url = record.get('url')
        if not url:
            print(f"Skipping record with missing URL: {record}")
            continue
        features = safe_extract_url_features(url)
        if features is not None:
            feature_list.append(features)
    except Exception as e:
        print(f"Error processing record {record}: {e}")
        continue

# Create a DataFrame from the list of feature dictionaries
if feature_list:
    X_train = pd.concat(feature_list, ignore_index=True)
    # Save the training data (X_train) to a file
    joblib.dump(X_train, 'X_train.pkl')
    print("Training data saved to X_train.pkl.")
else:
    print("No features extracted. X_train was not created.")
