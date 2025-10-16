import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler
from scipy.io import arff

# Load the .arff file using scipy
data, meta = arff.loadarff('C://Users//Govin//safesurf//backend//Training Dataset.arff')  # Use your actual file path

# Convert the data to a pandas DataFrame
df = pd.DataFrame(data)

# Step 1: Separate the features (X) and target (y)
X = df.drop(columns=['Result'])  # Drop the 'Result' column from features
y = df['Result']  # 'Result' is your target variable

# Step 2: Handle any preprocessing steps here (e.g., label encoding, NaN handling)
# Convert byte data columns to strings if necessary (since arff loads categorical data as byte arrays)
X = X.apply(lambda x: x.str.decode('utf-8') if x.dtype == 'object' else x)

# Step 3: Initialize the StandardScaler
scaler = StandardScaler()

# Step 4: Fit and transform the feature data
X_scaled = scaler.fit_transform(X)

# Step 5: Save the scaler for later use
joblib.dump(scaler, 'scaler.pkl')

# Optional: Save the scaled data or use it further
# pd.DataFrame(X_scaled).to_csv('scaled_data.csv', index=False)

print("Scaler saved as scaler.pkl")
