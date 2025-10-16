import pandas as pd
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib

# Loading the model and scaler
with open('random_forest_model.pkl', 'rb') as f:
    loaded_model = joblib.load(f)

with open('scaler.pkl', 'rb') as f:
    scaler = joblib.load(f)

# Preprocess the new data to match the training feature set
def preprocess_new_data(new_data):
    # Ensure that 'new_data' has the same columns as the training data
    # If new_data is a single data point, convert it to a DataFrame
    new_data_df = pd.DataFrame([new_data])

    # Apply the same scaling that was applied to the training data
    new_data_scaled = scaler.fit_transform(new_data_df)

    return new_data_scaled

# Example of new data (replace this with actual new data)
new_data = {
    'having_IP_Address': 1, 
    'URL_Length': 23, 
    'Shortining_Service': 0, 
    'having_At_Symbol': 1, 
    'double_slash_redirecting': 0, 
    'Prefix_Suffix': 0, 
    'having_Sub_Domain': 1, 
    'SSLfinal_State': 0, 
    'Domain_registeration_length': 10,
    'Favicon': 0,
    'port': 80,
    'HTTPS_token': 1,
    'Request_URL': 1,
    'URL_of_Anchor': 0,
    'Links_in_tags': 0,
    'SFH': 0,
    'Submitting_to_email': 0,
    'Abnormal_URL': 1,
    'Redirect': 0,
    'on_mouseover': 0,
    'RightClick': 0,
    'popUpWidnow': 0,
    'Iframe': 1,
    'age_of_domain': 5,
    'DNSRecord': 1,
    'web_traffic': 1,
    'Page_Rank': 0,
    'Google_Index': 1,
    'Links_pointing_to_page': 5,
    'Statistical_report': 0
}

# Preprocess and predict
new_data_scaled = preprocess_new_data(new_data)
prediction = loaded_model.predict(new_data_scaled)

# Output the result
print(f"Prediction for new data: {'Phishing' if prediction == 1 else 'Non-Phishing'}")
