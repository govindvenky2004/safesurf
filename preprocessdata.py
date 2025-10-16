import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
import nltk
from nltk.corpus import stopwords  # Add this import
import re
import joblib

# Download NLTK data (run once)
nltk.download('stopwords')

# Define preprocessing function
def preprocess_text(text):
    if not isinstance(text, str):  # Check if text is not a string
        return ""  # Return an empty string or a placeholder

    # Convert text to lowercase
    text = text.lower()

    # Remove special characters and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text)

    # Tokenize text and remove stopwords
    stop_words = set(stopwords.words('english'))
    words = text.split()
    filtered_words = [word for word in words if word not in stop_words]

    # Join words back into a single string
    return ' '.join(filtered_words)

# Extract email features like length of body, presence of URL, and keywords
def extract_email_features(text):
    # Initialize feature dictionary
    features = {}
    
    # Check if the email contains a URL
    features['contains_url'] = int(bool(re.search(r'http[s]?://', text)))
    
    # Check the length of the email body (number of words)
    features['email_length'] = len(text.split())
    
    # Check for common phishing keywords
    phishing_keywords = ['urgent', 'account', 'verify', 'password', 'click here', 'login', 'confirm', 'suspicious']
    features['contains_phishing_keywords'] = int(any(keyword in text for keyword in phishing_keywords))
    
    return features

# Folder containing CSV files
folder_path = r'C:\Users\Govin\safesurf\backend\archive'  # Replace with your folder path

# Initialize an empty list to hold data
all_data = []

# Loop through all files in the folder
for file in os.listdir(folder_path):
    if file.endswith('.csv'):
        file_path = os.path.join(folder_path, file)
        
        # Try loading the data and ensure necessary columns exist
        try:
            data = pd.read_csv(file_path)
            print(f"Columns in {file}: {data.columns}")  # Print the columns of each file
            
            # If 'text_combined' exists, append the data
            if 'text_combined' in data.columns:
                all_data.append(data)
            
            # If 'text_combined' is missing, combine other columns into a text field
            else:
                if 'subject' in data.columns and 'body' in data.columns:
                    # Convert columns to strings before concatenating
                    data['text_combined'] = data['subject'].astype(str) + ' ' + data['body'].astype(str)
                    if 'urls' in data.columns:
                        data['text_combined'] += ' ' + data['urls'].astype(str)
                    all_data.append(data)
                else:
                    print(f"Skipping {file} - Missing necessary columns.")
        
        except Exception as e:
            print(f"Error loading {file}: {e}")

# Combine all data into a single DataFrame
if all_data:
    combined_data = pd.concat(all_data, ignore_index=True)

    # Drop rows with missing values in important columns
    combined_data.dropna(subset=['text_combined', 'label'], inplace=True)

    # Ensure label is binary (0 or 1), just in case there are any missing/incorrect values
    if 'label' in combined_data.columns:
        combined_data['label'] = combined_data['label'].apply(lambda x: 1 if x > 0 else 0)
    else:
        print("Warning: 'label' column is missing in some datasets, setting default labels to 0.")
        combined_data['label'] = 0  # Assuming default label for missing 'label' columns
    
    # Preprocess the text column
    combined_data['processed_text'] = combined_data['text_combined'].apply(preprocess_text)

    # Apply SimpleImputer to handle missing values in the 'processed_text' column
    # Apply SimpleImputer to handle missing values
    # Apply SimpleImputer to handle missing values
    imputer = SimpleImputer(strategy='constant', fill_value='missing')

# Ensure the 'processed_text' column is in 2D format (as DataFrame) for the imputer
    processed_text = combined_data[['processed_text']]

# Impute missing values
    combined_data['processed_text'] = imputer.fit_transform(processed_text).flatten()


    # Drop rows where 'processed_text' is empty or NaN
    combined_data = combined_data[combined_data['processed_text'].notna() & (combined_data['processed_text'] != '')]

    # Extract email features
    email_features = combined_data['text_combined'].apply(extract_email_features)
    email_features_df = pd.json_normalize(email_features)

    # Concatenate email features with the processed text data
    combined_data = pd.concat([combined_data, email_features_df], axis=1)

    # Vectorize the processed text using TF-IDF
    vectorizer = TfidfVectorizer(max_features=5000)
    X_text = vectorizer.fit_transform(combined_data['processed_text'])

    # Combine the TF-IDF features with the extracted email features
    X = pd.concat([pd.DataFrame(X_text.toarray()), email_features_df], axis=1)

    # Target variable
    y = combined_data['label']

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Save the preprocessed data and vectorizer
    joblib.dump((X_train, X_test, y_train, y_test), 'preprocessed_data.pkl')
    joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')

    print("Preprocessing complete, data saved.")
else:
    print("No valid data found for preprocessing.")
