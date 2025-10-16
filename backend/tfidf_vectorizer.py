import re
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

# Example function for extracting features from email body
def extract_email_features(email_body, vectorizer=None):
    # Preprocess the email body text (removing unnecessary characters, etc.)
    email_body = clean_text(email_body)
    
    # Initialize the list of features
    features = []
    
    # Example of predefined features you might want to extract
    features.append(count_links(email_body))  # Feature 1: Number of links in the email
    features.append(count_words(email_body))  # Feature 2: Word count in the email
    features.append(avg_word_length(email_body))  # Feature 3: Average word length in the email
    # Add more predefined features as needed

    if vectorizer is None:
        # Create and fit the vectorizer if not provided
        vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        tfidf_features = vectorizer.fit_transform([email_body]).toarray()
        
        # Save the fitted vectorizer for later use
        joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')
    else:
        # If a vectorizer is passed, use it to transform the text
        tfidf_features = vectorizer.transform([email_body]).toarray()

    # Append the TF-IDF features to the list of predefined features
    features.extend(tfidf_features[0])  # Add the top features from TF-IDF (the output should be 1000 features)
    
    # Make sure we only return the first 9 features (you can adjust which features to keep)
    features = features[:9]  # Adjust if you need to include more from TF-IDF or less

    # Return the 9 features as a list
    return features, vectorizer

def clean_text(text):
    # Clean the text by removing non-alphabetic characters and extra spaces
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def count_links(text):
    # Count the number of links in the email
    return len(re.findall(r'http[s]?://\S+', text))  # Regex to count URLs

def count_words(text):
    # Count the number of words in the email
    return len(text.split())  # Split the text into words and count

def avg_word_length(text):
    # Calculate the average word length in the email
    words = text.split()
    return sum(len(word) for word in words) / len(words) if words else 0

# Example of processing the dataset (assuming the dataset is loaded as a pandas DataFrame)

import pandas as pd

# Assuming you have loaded your CSVs into pandas DataFrames
df = pd.read_csv('phishing_email.csv')  # Replace with your actual file

# Previewing the data
print(df.head())  # Check the first 5 rows to ensure it's loaded properly

# Extract features for each email in the dataset
email_features = []
vectorizer = None  # Vectorizer will be created or used depending on the first email

for index, row in df.iterrows():
    email_body = row['body']  # Extract the 'body' of the email
    features, vectorizer = extract_email_features(email_body, vectorizer)
    email_features.append(features)

# Convert the list of features into a DataFrame for easy inspection
features_df = pd.DataFrame(email_features)

# View the first few rows of the extracted features
print(features_df.head())

# Save the extracted features to a CSV file if needed
features_df.to_csv('extracted_features.csv', index=False)

