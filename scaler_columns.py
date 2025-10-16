import joblib
import pandas as pd

# Manually specify the column names (these should be the same as during training)
expected_columns = [
    'having_IP_Address', 'URL_Length', 'Shortining_Service', 'having_At_Symbol', 'double_slash_redirecting', 
    'Prefix_Suffix', 'having_Sub_Domain', 'SSLfinal_State', 'Domain_registeration_length', 'Favicon', 'port', 
    'HTTPS_token', 'Request_URL', 'URL_of_Anchor', 'Links_in_tags', 'SFH', 'Submitting_to_email', 'Abnormal_URL', 
    'Redirect', 'on_mouseover', 'RightClick', 'popUpWidnow', 'Iframe', 'age_of_domain', 'DNSRecord', 'web_traffic', 
    'Page_Rank', 'Google_Index', 'Links_pointing_to_page', 'Statistical_report'
]

# Save the column names to a .pkl file
joblib.dump(expected_columns, 'scaler_columns.pkl')
