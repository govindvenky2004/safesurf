import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from imblearn.over_sampling import SMOTE
from sklearn.impute import SimpleImputer
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.io import arff

# Step 1: Load the raw dataset (assuming the raw data is in 'raw_data.arff')
data, meta = arff.loadarff('C://Users//Govin//safesurf//backend//Training Dataset.arff')
df = pd.DataFrame(data)  # Convert ARFF data to a DataFrame

# Step 2: Initial Inspection
print(f"Dataset Shape: {df.shape}")
print(f"Missing Values:\n{df.isnull().sum()}")
print(f"Initial Class Distribution:\n{df['Result'].value_counts()}")

# Step 3: Handle Missing Values in Features (if any)
# Use SimpleImputer to fill missing values for numerical columns
imputer = SimpleImputer(strategy='mean')  # You can also use 'median' if preferred
df_imputed = df.copy()

# Apply imputer to all columns except the 'Result' column
df_imputed[df_imputed.columns.difference(['Result'])] = imputer.fit_transform(df_imputed[df_imputed.columns.difference(['Result'])])

# Handle missing values in 'Result' column (target variable)
# Fill NaNs with mode of 'Result' column
mode_result = df_imputed['Result'].mode()[0]
df_imputed['Result'].fillna(mode_result, inplace=True)

print(f"Missing Values After Imputation:\n{df_imputed.isnull().sum()}")

# Step 4: Map the 'Result' Column to Binary Values (if needed)
# Assume '1' represents phishing (1), '-1' represents non-phishing (0)
df_imputed['Result'] = df_imputed['Result'].map({b'1': 1, b'-1': 0})

# Ensure no NaN values after mapping
df_imputed['Result'].fillna(df_imputed['Result'].mode()[0], inplace=True)

print(f"Unique values in 'Result' after mapping: {df_imputed['Result'].unique()}")

# Step 5: Convert Features to Numeric (if any non-numeric)
# Ensure all feature columns are numeric
df_imputed = df_imputed.apply(pd.to_numeric, errors='coerce')

# Step 6: Handle Class Imbalance using SMOTE
# Split features (X) and target (y)
X = df_imputed.drop(columns=['Result'])
y = df_imputed['Result']

# Check if there are any NaN values in target column 'y'
print(f"NaN values in target column: {y.isnull().sum()}")

# Step 7: Split the dataset into training and testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Step 8: Apply SMOTE to handle class imbalance
smote = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

print(f"Class distribution after SMOTE:\n{y_train_resampled.value_counts()}")

# Step 9: Feature Scaling using StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_resampled)
X_test_scaled = scaler.transform(X_test)

# Step 10: Outlier Detection (Optional, but recommended)
# Visualize outliers using boxplots to check for extreme values
for column in X.columns:
    plt.figure(figsize=(8, 6))
    sns.boxplot(x=X[column])
    plt.title(f'Boxplot for {column}')
    plt.show()

# Step 11: Final Preprocessing Summary
print(f"Shape of Preprocessed X_train: {X_train_scaled.shape}")
print(f"Shape of Preprocessed X_test: {X_test_scaled.shape}")
print(f"Final Class Distribution in y_train:\n{y_train_resampled.value_counts()}")
