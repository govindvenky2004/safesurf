import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# Load the dataset
dataset_path = "C://Users//Govin//safesurf//backend//Phising_Testing_Dataset.csv" # Update this with the actual path to your downloaded CSV
data = pd.read_csv(dataset_path)

# Data scaling
scaler = StandardScaler()
numerical_features = data.select_dtypes(include=['int64', 'float64']).columns
data[numerical_features] = scaler.fit_transform(data[numerical_features])

# Splitting into features (X) and target (y)
X = data.drop(columns=['Statistical_report'])  # Replace 'result' with the actual target column name if different
y = data['Statistical_report']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# You can print shapes to confirm
print(f"Training data shape: {X_train.shape}")
print(f"Testing data shape: {X_test.shape}")
