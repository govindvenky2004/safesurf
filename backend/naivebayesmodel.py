import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, f1_score, classification_report, ConfusionMatrixDisplay, confusion_matrix
import joblib
from sklearn.impute import SimpleImputer  # Import the SimpleImputer

# Suppress warnings
import warnings
warnings.filterwarnings('ignore')

# Load the dataset
df = pd.read_csv("C://Users//Govin//safesurf//backend//Phishing_Email.csv")

# Display the first few rows of the dataset
print("Initial Dataset Preview:")
print(df.head())

# Check for missing values
print("\nMissing Values in Each Column:")
print(df.isnull().sum())

# Data cleaning
df.drop(["Unnamed: 0"], axis=1, inplace=True)  # Drop unnecessary column

# Handle missing values in the 'Email Text' column by replacing them with a placeholder text
df['Email Text'].fillna('missing', inplace=True)

df.drop_duplicates(inplace=True)  # Remove duplicate rows

# Print dataset dimensions after cleaning
print("\nDimensions of the cleaned dataset:", df.shape)

# Check the first few rows after cleaning
print("\nCleaned Dataset Preview:")
print(df.head())

# Label encoding for the 'Email Type' column
le = LabelEncoder()
df["Email Type"] = le.fit_transform(df["Email Type"])

# Check the updated dataset with encoded labels
print("\nDataset after Label Encoding:")
print(df.head())

# Uncomment the following section to visualize category distribution
"""
# Bar chart of category distribution
fig = px.bar(
    x=df['Email Type'].value_counts().index,
    y=df['Email Type'].value_counts().values,
    color=df['Email Type'].value_counts().index,
    labels={'x': 'Category', 'y': 'Count'},
    title="Categorical Distribution (Bar Chart)"
)
fig.show()


# Pie chart of category distribution
fig_pie = px.pie(
    names=df['Email Type'].value_counts().index,
    values=df['Email Type'].value_counts().values,
    title="Categorical Distribution (Pie Chart)"
)
fig_pie.show()
"""
"""from wordcloud import WordCloud

#combine all rows into a single string
all_mails = " ".join(df['Email Text'])

#create a wordcloud object
word_cloud = WordCloud(stopwords="english",width=800,height=400,background_color='white').generate(all_mails)

plt.figure(figsize=(10,6))
plt.imshow(word_cloud,interpolation='bilinear')
plt.axis("off")
plt.show()
all_mails = " ".join(df['Email Text'])

#create a wordcloud object
word_cloud = WordCloud(width=800,height=400,background_color='white',max_words=10000).generate(all_mails)
plt.figure(figsize=(10,6))
plt.imshow(word_cloud,interpolation='bilinear')
plt.axis("off")
plt.show()"""
tf = TfidfVectorizer(stop_words="english",max_features=10000) #dimension reduction

feature_x = tf.fit_transform(df["Email Text"]).toarray()
y_tf = np.array(df['Email Type']) # convert the label into numpy array
x_train,x_test,y_train,y_test = train_test_split(feature_x,y_tf,train_size=0.8,random_state=0)

nb = MultinomialNB()
nb.fit(x_train,y_train)

pred_nav = nb.predict(x_test)

# Checking the performance

print(f"accuracy from native bayes: {accuracy_score(y_test,pred_nav)*100:.2f} %")
print(f"f1 score from naive bayes: {f1_score(y_test,pred_nav)*100:.2f} %")
print("classification report :\n\n",classification_report(y_test,pred_nav))

#confusion matrix
clf_nav = confusion_matrix(y_test,pred_nav)
cx_ = ConfusionMatrixDisplay(clf_nav,display_labels=['pishing_mail','safe_mail']).plot()
plt.show()

joblib.dump(nb,'naive_bayes_model.pkl')
joblib.dump(tf,'tfidf_vectorizer.pkl')
