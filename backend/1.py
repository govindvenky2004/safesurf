import joblib
import pandas as pd

# Load the trained RandomForest model and scaler
model = joblib.load('random_forest_model.pkl')
scaler = joblib.load('scaler.pkl')

# Extract the feature names used in the training of the model (if available)
trained_feature_names = model.feature_names_in_ if hasattr(model, 'feature_names_in_') else None

# If model feature names are not available, manually define them
if trained_feature_names is None:
    trained_feature_names = ['Abnormal_URL', 'HTTPS_token', 'having_IP', 'key', 'port',
                             'URL_Length', 'Shortining_Service', 'having_At_Symbol', 'double_slash_redirecting', 
                             'Prefix_Suffix', 'having_Sub_Domain', 'SSLfinal_State', 'Domain_registeration_length', 
                             'Favicon', 'Request_URL', 'URL_of_Anchor', 'Links_in_tags', 'SFH', 'Submitting_to_email', 
                             'Redirect', 'on_mouseover', 'RightClick', 'popUpWidnow', 'Iframe', 'age_of_domain', 
                             'DNSRecord', 'web_traffic', 'Page_Rank', 'Google_Index', 'Links_pointing_to_page', 'Statistical_report']

# Input data as a dictionary (ensure it includes all the necessary features)
feature_values = {'Abnormal_URL': 0, 'HTTPS_token': 0, 'having_IP': 1, 'key': 0, 'port': 0,
                  'URL_Length': 17, 'Shortining_Service': -1, 'having_At_Symbol': -1, 
                  'double_slash_redirecting': 1, 'Prefix_Suffix': 1, 'having_Sub_Domain': 0, 
                  'SSLfinal_State': 0, 'Domain_registeration_length': 1, 'Favicon': -1, 
                  'Request_URL': 1, 'URL_of_Anchor': 1, 'Links_in_tags': 1, 'SFH': 1, 
                  'Submitting_to_email': -1, 'Redirect': 0, 'on_mouseover': -1, 'RightClick': -1, 
                  'popUpWidnow': -1, 'Iframe': -1, 'age_of_domain': 1, 'DNSRecord': 1, 'web_traffic': 1, 
                  'Page_Rank': 1, 'Google_Index': 1, 'Links_pointing_to_page': 1, 'Statistical_report': 1}

# Convert the dictionary to a DataFrame
input_df = pd.DataFrame([feature_values])

# Ensure the input DataFrame has the columns in the same order as the trained model
input_df = input_df[trained_feature_names]

# Apply the scaler to the input data
input_scaled = scaler.transform(input_df)

# Predict with the model
prediction = model.predict(input_scaled)

# Output the prediction
print("Prediction (0 for non-phishing, 1 for phishing):", prediction)
