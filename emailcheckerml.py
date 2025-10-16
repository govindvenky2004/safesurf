import imaplib
import email
from email import policy
import re
import logging
import joblib
import getpass
import msvcrt

# Set up logging
logging.basicConfig(filename='email_analysis_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

# Global variable to track if any threats were detected
threat_found = False

# Function to securely input a password
def input_password(prompt="Enter password: "):
    print(prompt, end='', flush=True)
    password = ''
    while True:
        char = msvcrt.getch()
        if char == b'\r':  # Enter key
            break
        elif char == b'\x08':  # Backspace key
            if len(password) > 0:
                password = password[:-1]
                print("\b \b", end='', flush=True)
        else:
            password += char.decode('utf-8')
            print('*', end='', flush=True)
    print()
    return password

# Function to extract URLs from email content
def extract_urls_from_email(content):
    url_pattern = r'(https?://[^\s]+)'
    return re.findall(url_pattern, content)

# Function to load the pre-trained Naive Bayes model and vectorizer
def load_naive_bayes_model():
    try:
        model = joblib.load("naive_bayes_model.pkl")
        vectorizer = joblib.load("tfidf_vectorizer.pkl")
        return model, vectorizer
    except Exception as e:
        logging.error(f"Error loading model or vectorizer: {e}")
        raise

# Function to check a URL using the Naive Bayes classifier
def check_url(url, model, vectorizer):
    global threat_found
    try:
        url_vect = vectorizer.transform([url])
        prediction = model.predict(url_vect)
        if prediction == 1:
            result = f"Threat detected for URL: {url}"
            threat_found = True
        else:
            result = f"No threat detected for URL: {url}"
        logging.info(result)
        print(result)
    except Exception as e:
        logging.error(f"Error analyzing URL: {url} - {e}")

# Function to process each email
def process_email(email_id, mail, model, vectorizer):
    try:
        status, email_data = mail.fetch(email_id, "(RFC822)")
        if status != 'OK':
            logging.error(f"Failed to fetch email ID {email_id}")
            return

        raw_email = email_data[0][1]
        msg = email.message_from_bytes(raw_email, policy=policy.default)

        # Log email metadata
        sender = msg.get('From', 'Unknown Sender')
        subject = msg.get('Subject', 'No Subject')
        logging.info(f"Processing email from: {sender}, Subject: {subject}")

        # Extract email content
        email_body = ""
        if msg.is_multipart():
            for part in msg.iter_parts():
                if part.get_content_type() == "text/plain":
                    email_body += part.get_payload(decode=True).decode(errors='ignore')
                elif part.get_content_type() == "text/html":
                    email_body += part.get_payload(decode=True).decode(errors='ignore')
        else:
            email_body = msg.get_payload(decode=True).decode(errors='ignore')

        # Log extracted email content
        logging.info(f"Extracted email content: {email_body[:100]}...")

        # Extract and analyze URLs
        urls = extract_urls_from_email(email_body)
        if not urls:
            logging.info("No URLs found in email.")
            return

        for url in urls:
            check_url(url, model, vectorizer)

        # Mark email as read
        mail.store(email_id, '+FLAGS', '\\Seen')

    except Exception as e:
        logging.error(f"Error processing email ID {email_id}: {e}")

# Function to fetch and process emails
def fetch_emails(model, vectorizer):
    EMAIL = input("Enter your email: ")
    PASSWORD = input_password()
    
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(EMAIL, PASSWORD)

        # Choose the mailbox to analyze
        categories = {"1": "inbox", "2": "[Gmail]/Promotions", "3": "[Gmail]/Spam"}
        print("Choose the mailbox to analyze:")
        for key, category in categories.items():
            print(f"{key}. {category}")
        choice = input("Enter your choice (default is Inbox): ") or "1"
        mailbox = categories.get(choice, "inbox")

        # Select the mailbox
        mail.select(mailbox)

        # Search for unread emails
        status, email_ids = mail.search(None, "UNSEEN")
        if status != 'OK' or not email_ids[0]:
            logging.info("No unread emails found.")
            print("No unread emails found.")
            return False

        email_ids = email_ids[0].split()
        print(f"Found {len(email_ids)} unread emails. Processing...")
        for i, email_id in enumerate(email_ids, start=1):
            print(f"Processing email {i}/{len(email_ids)}...")
            process_email(email_id, mail, model, vectorizer)

        return True if threat_found else False

    except imaplib.IMAP4.error as e:
        logging.error(f"IMAP error: {e}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return False
    finally:
        try:
            mail.logout()
            print("Logged out successfully.")
        except Exception as e:
            logging.error(f"Error during logout: {e}")

# Main function
def main():
    try:
        model, vectorizer = load_naive_bayes_model()
        print("Starting email analysis...")
        threats = fetch_emails(model, vectorizer)

        if threats:
            print("Threats detected! Check the log for details.")
        else:
            print("No threats detected. All emails are safe.")
        print("Analysis complete.")

    except Exception as e:
        logging.error(f"Fatal error: {e}")
        print("An error occurred. Please check the logs.")

if __name__ == "__main__":
    main()
