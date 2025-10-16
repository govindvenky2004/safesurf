from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

# Create and configure the TfidfVectorizer
vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(2, 5), max_features=3000)

# Example: Fit the vectorizer on training data
# Assuming 'training_urls' is a list of URLs for training your model
training_urls = [
    "http://example.com",
    "https://malicious.com",
    "http://safewebsite.com"
    # Add more URLs here
]

# Fit the vectorizer on the training URLs and transform them
X_train = vectorizer.fit_transform(training_urls)

# Example labels for your training data (1 for phishing, 0 for non-phishing)
y_train = [0, 1, 0]  # Add corresponding labels

# Now you can train a RandomForest model (or any model) with the transformed data
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save the trained model and vectorizer for future use
joblib.dump(model, 'random_forest_model.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')

print("Model and Vectorizer saved!")
