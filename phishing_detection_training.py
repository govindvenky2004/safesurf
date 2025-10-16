import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer

# Step 1: Load Data
from scipy.io import arff

# Load the dataset from the ARFF file
data, meta = arff.loadarff('C://Users//Govin//safesurf//backend//Training Dataset.arff')
df = pd.DataFrame(data)

# Step 2: Initial Inspection
print(f"Dataset Shape: {df.shape}")
print(f"Missing Values:\n{df.isnull().sum()}")
print(f"Initial Class Distribution:\n{df['Result'].value_counts()}")

# Step 3: Handle Missing Values in Features
imputer = SimpleImputer(strategy='mean')
df_imputed = df.copy()
df_imputed[df_imputed.columns.difference(['Result'])] = imputer.fit_transform(df_imputed[df_imputed.columns.difference(['Result'])])

# Handle missing values in 'Result' column (target variable)
df_imputed['Result'].fillna(df_imputed['Result'].mode()[0], inplace=True)

print(f"Missing Values After Imputation:\n{df_imputed.isnull().sum()}")

# Step 4: Map 'Result' Column to Binary
label_mapping = {b'-1': 0, b'1': 1}  # Map to 0 and 1
df_imputed['Result'] = df_imputed['Result'].map(label_mapping)

print(f"Unique values in 'Result' after mapping: {df_imputed['Result'].unique()}")

# Step 5: Convert Features to Numeric
df_imputed = df_imputed.apply(pd.to_numeric, errors='coerce')

# Step 6: Split Data into Features (X) and Target (y)
X = df_imputed.drop(columns=['Result'])
y = df_imputed['Result']

# Step 7: Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Step 8: Handle Class Imbalance using SMOTE
smote = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

print(f"Class distribution after SMOTE:\n{y_train_resampled.value_counts()}")

# Step 9: Feature Scaling using StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_resampled)
X_test_scaled = scaler.transform(X_test)

# Step 10: Choose and Train the Model
model = LogisticRegression(random_state=42)  # Or use RandomForestClassifier() or any other classifier

# Train the model
model.fit(X_train_scaled, y_train_resampled)

# Step 11: Predict on the Test Set
y_pred = model.predict(X_test_scaled)

# Step 12: Evaluate the Model
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.4f}")

# Print classification report
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Confusion Matrix
conf_matrix = confusion_matrix(y_test, y_pred)
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=["Non-Phishing", "Phishing"], yticklabels=["Non-Phishing", "Phishing"])
plt.title('Confusion Matrix')
plt.ylabel('True Label')
plt.xlabel('Predicted Label')
plt.show()
