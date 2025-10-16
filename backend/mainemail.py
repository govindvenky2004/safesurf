import imaplib
import email
from email.header import decode_header
import re
import joblib
import nltk
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from getpass import getpass  # To securely get the password input
from url_features import extract_url_features
import msvcrt

def input_password(prompt="Enter password: "):
    print(prompt, end='', flush=True)
    password = ''
    while True:
        char = msvcrt.getch()  # Get the character input
        if char == b'\r':  # Enter key
            break
        elif char == b'\x08':  # Backspace key
            password = password[:-1]
            print("\b \b", end='', flush=True)  # Move cursor back and replace with space
        else:
            password += char.decode('utf-8')
            print('*', end='', flush=True)  # Display asterisk for each character
    print()  # Move to the next line after password input
    return password



# Function to validate email format
def validate_email(email):
    # Regular expression for basic email validation
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(email_regex, email):
        return True
    else:
        return False

# Function to validate password (example: length >= 8, must contain letters and numbers)
def validate_password(password):
    if len(password) >= 8 and re.search(r'[A-Za-z]', password) and re.search(r'[0-9]', password):
        return True
    return False

# Function to preprocess email text
def preprocess_email(text):
    if not isinstance(text, str):  # Check if text is not a string
        return ""  # Return an empty string or a placeholder

    # Convert text to lowercase
    text = text.lower()

    # Remove special characters and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text)

    # Tokenize text and remove stopwords (if necessary)
    stop_words = set(nltk.corpus.stopwords.words('english'))
    words = text.split()
    filtered_words = [word for word in words if word not in stop_words]

    # Join words back into a single string
    return ' '.join(filtered_words)



def fetch_emails(email_id, email_password):
    # Connect to the mail server
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(email_id, email_password)

    # Select the mailbox you want to use (INBOX in this case)
    mail.select("inbox")

    # Search for all emails
    status, messages = mail.search(None, "ALL")
    email_ids = messages[0].split()

    # Loop through each email ID
    for email_id in email_ids:
        # Fetch the email
        status, msg_data = mail.fetch(email_id, "(RFC822)")
        
        # Loop through the email parts
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])

                # Decode email subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")

                # Decode email sender
                from_ = msg.get("From")

                # Print subject and sender
                print(f"Subject: {subject}")
                print(f"From: {from_}")

                # Check if the email message has multiple parts
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))

                        # If the part is text/plain or text/html
                        if "attachment" not in content_disposition:
                            # Get the body
                            body = part.get_payload(decode=True)
                            if body:  # Ensure body is not None
                                try:
                                    body = body.decode()
                                    print(f"Body: {body[:500]}...")  # Print the first 500 characters of the email body
                                except Exception as e:
                                    print(f"Error decoding body: {e}")
                else:
                    # For non-multipart emails (rare, but possible)
                    body = msg.get_payload(decode=True)
                    if body:  # Ensure body is not None
                        try:
                            body = body.decode()
                            print(f"Body: {body[:500]}...")  # Print the first 500 characters of the email body
                        except Exception as e:
                            print(f"Error decoding body: {e}")

    mail.logout()

# Function to check URL in real-time
def check_url(url_to_check):
    # Extract features for the URL
    features = extract_url_features(url_to_check)

    # Ensure the features are in a 2D array (1 row, n_features columns)
    features_reshaped = np.array(features).reshape(1, -1)

    # Predict using the loaded model
    prediction = model.predict(features_reshaped)

    # Output the prediction
    print(f"Prediction for the URL: {'Phishing' if prediction[0] == 1 else 'Legitimate'}")

# Get email and password input securely
email_id = input("Enter your email: ")
while not validate_email(email_id):
    print("Invalid email format. Please enter a valid email address.")
    email_id = input("Enter your email: ")
# Usage
email_password = input_password("Enter your email password: ")
#print("Password entered:", email_password)
#while not validate_password(email_password):
    #print("Password must be at least 8 characters long and contain both letters and numbers.")
    #email_password = getpass("Enter your email password: ")

# Load model and vectorizer
model = joblib.load('naive_bayes_model.pkl')
vectorizer = joblib.load('tfidf_vectorizer.pkl')

# Example real-time email check
fetch_emails(email_id, email_password)

# Example real-time URL check
check_url("http://currently210.weebly.com/")  # Replace with an actual URL
