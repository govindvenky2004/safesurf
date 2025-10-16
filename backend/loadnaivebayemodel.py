import joblib
import numpy as np
from url_features2 import extract_url_features2  # Import your feature extraction function

# Load the saved model and vectorizer
model = joblib.load('naive_bayes_model.pkl')
vectorizer = joblib.load('tfidf_vectorizer.pkl')  # Load the vectorizer

# Example URL to check
url_to_check = 'http://example.com/login'  # Replace with an actual URL

# Extract URL features (numeric features, if necessary)
features = extract_url_features2(url_to_check)

# If the features are text-based, use the vectorizer to convert them to the expected format
features_transformed = vectorizer.transform([str(features)])  # Transform to match the vectorizer input

# Predict using the loaded model
prediction = model.predict(features_transformed)

# Output the prediction
print(f"Prediction for the URL: {'Phishing' if prediction[0] == 1 else 'Legitimate'}")
