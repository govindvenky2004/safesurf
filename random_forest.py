import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.io import arff
import joblib

# Step 1: Load the raw dataset (ensure the path is correct)
data, meta = arff.loadarff(r'C://Users//Govin//safesurf//backend//Training Dataset.arff')
df = pd.DataFrame(data)

# Initial Inspection
print(f"Dataset Shape: {df.shape}")
print(f"Dataset Columns: {df.columns}")
print(f"Missing Values:\n{df.isnull().sum()}")
print(f"Initial Class Distribution:\n{df['Result'].value_counts()}")

# Step 2: Handle Missing Values in Features (if any)
# Use SimpleImputer to fill missing values for numerical columns
imputer = SimpleImputer(strategy='mean')  # You can also use 'median' if preferred
df_imputed = df.copy()
df_imputed[df_imputed.columns.difference(['Result'])] = imputer.fit_transform(df_imputed[df_imputed.columns.difference(['Result'])])

# Handle missing values in 'Result' column (target variable)
mode_result = df_imputed['Result'].mode()[0]
df_imputed['Result'].fillna(mode_result, inplace=True)

print(f"Missing Values After Imputation:\n{df_imputed.isnull().sum()}")

# Step 3: Map the 'Result' Column (ensure binary values for phishing detection)
df_imputed['Result'] = df_imputed['Result'].replace({b'-1': 0, b'1': 1})  # Ensure this matches your dataset format

# Check unique values in 'Result' after mapping
print(f"Unique values in 'Result' after mapping: {df_imputed['Result'].unique()}")

# Step 4: Convert Features to Numeric (if any non-numeric columns)
# Check for non-numeric columns and handle them appropriately
non_numeric_columns = df_imputed.select_dtypes(include=['object']).columns
print(f"Non-numeric columns: {non_numeric_columns}")

# For simplicity, handle categorical columns with one-hot encoding or label encoding (depending on the dataset)
df_imputed = pd.get_dummies(df_imputed, columns=non_numeric_columns, drop_first=True)

# Ensure all features are numeric after conversion
df_imputed = df_imputed.apply(pd.to_numeric, errors='coerce')  # Convert non-numeric to NaN

# Step 5: Handle Class Imbalance using SMOTE
X = df_imputed.drop(columns=['Result'])
y = df_imputed['Result']

# Ensure there are no missing values in the target column 'y'
assert y.isnull().sum() == 0, "There are still missing values in the target column!"

# Split the dataset into training and testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Apply SMOTE to handle class imbalance
smote = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

print(f"Class distribution after SMOTE:\n{y_train_resampled.value_counts()}")

# Step 6: Feature Scaling using StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_resampled)
X_test_scaled = scaler.transform(X_test)

# Reindex the test set to match the training set columns (fix feature mismatch)
X_test_scaled = pd.DataFrame(X_test_scaled, columns=X_train.columns)
X_test_scaled = X_test_scaled.reindex(columns=X_train.columns, fill_value=0)

# Step 7: Train the Random Forest model
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train_scaled, y_train_resampled)

# Step 8: Evaluate the model performance
y_pred_rf = rf_model.predict(X_test_scaled)

# Accuracy
accuracy_rf = accuracy_score(y_test, y_pred_rf)
print(f"Random Forest Accuracy: {accuracy_rf:.4f}")

# Classification Report
print("Classification Report for Random Forest:")
print(classification_report(y_test, y_pred_rf))

# Confusion Matrix
conf_matrix_rf = confusion_matrix(y_test, y_pred_rf)
print("Confusion Matrix for Random Forest:")
print(conf_matrix_rf)

# Optional: Visualizing the confusion matrix using heatmap
sns.heatmap(conf_matrix_rf, annot=True, fmt='d', cmap='Blues', xticklabels=['Non-Phishing', 'Phishing'], yticklabels=['Non-Phishing', 'Phishing'])
plt.title('Random Forest Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show()

# Step 9: Saving the trained model
model_filename = 'random_forest_model.pkl'
joblib.dump(rf_model, model_filename)
print(f"Model saved as {model_filename}")

# Step 10: Loading the saved model for future predictions
loaded_model = joblib.load(model_filename)
print("Model loaded successfully.")
