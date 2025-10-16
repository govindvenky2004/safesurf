import imaplib
import email
from email import policy
import re
import requests
import concurrent.futures
import logging

# Google Safe Browsing API Key
API_KEY = 'AIzaSyCytvF0mIdAT_dPHTlKjHIXpWAPummbeCI'

# Set up logging
logging.basicConfig(filename='email_analysis_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

# Variable to track if any threats were detected
threat_found = False

# Function to extract URLs from the email body
def extract_urls_from_email(email_content):
    url_pattern = r'(https?://[^\s]+)'
    urls = re.findall(url_pattern, email_content)
    return urls

# Function to check URL using Google Safe Browsing API
def check_url(url_to_check):
    global threat_found  # Access the global variable to update its state

    payload = {
        "client": {
            "clientId": "your_client_id",
            "clientVersion": "1.5.2"
        },
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url_to_check}]
        }
    }

    response = requests.post(
        f'https://safebrowsing.googleapis.com/v4/threatMatches:find?key={API_KEY}',
        json=payload
    )

    data = response.json()

    if data.get('matches'):
        result = f"Threat detected for URL: {url_to_check}"
        threat_found = True  # Update the global variable if a threat is detected
    else:
        result = f"No threat detected for URL: {url_to_check}"

    # Log the result without printing to the console
    logging.info(result)

# Connect to Gmail using IMAP and fetch emails
def fetch_emails():
    # Email login credentials
    EMAIL = "govindvenkatesh2004@gmail.com"  # Replace with your email
    PASSWORD = "cdzz azfs ewba huqp"  # Use an App Password if 2FA is enabled
    
    try:
        # Connect to Gmail's IMAP server
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(EMAIL, PASSWORD)
        
        # Select the mailbox you want to use ('inbox' in this case)
        mail.select("inbox")
        
        # Search for unread emails only (avoid processing all emails)
        status, email_ids = mail.search(None, "UNSEEN")
        
        # Get the list of email IDs
        email_ids = email_ids[0].split()
        
        # Process emails
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Create a list of tasks for processing emails
            futures = [executor.submit(process_email, email_id, mail) for email_id in email_ids]
            
            # Wait for all futures to complete
            for future in concurrent.futures.as_completed(futures):
                future.result()

    except imaplib.IMAP4.abort as e:
        print(f"Error occurred while interacting with the IMAP server: {e}")
    
    finally:
        try:
            # Ensure the connection is properly closed
            if 'mail' in locals():
                mail.logout()
                print("Logged out successfully.")
        except Exception as e:
            print(f"Error during logout: {e}")

# Function to process each email
def process_email(email_id, mail):
    status, email_data = mail.fetch(email_id, "(RFC822)")
    raw_email = email_data[0][1]
        
    # Parse the email content
    msg = email.message_from_bytes(raw_email, policy=policy.default)
        
    # Extract the email body content (handling multipart emails)
    if msg.is_multipart():
        for part in msg.iter_parts():
            if part.get_content_type() == "text/plain":
                email_body = part.get_payload(decode=True).decode()
                break
    else:
        email_body = msg.get_payload(decode=True).decode()

    # Extract URLs from the email body
    urls = extract_urls_from_email(email_body)

    # Check each URL using the Safe Browsing API in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit each URL check as a separate task
        futures = [executor.submit(check_url, url) for url in urls]
        
        # Wait for all futures to complete
        for future in concurrent.futures.as_completed(futures):
            future.result()
    
    # Mark email as read after processing
    mail.store(email_id, '+FLAGS', '\\Seen')

# Main function to start the process
def main():
    # Inform the user that the process is starting
    print("Processing unread emails. Please wait...")

    fetch_emails()

    # Final status check and message to the user
    if threat_found:
        print("Threats were detected in one or more emails. Please check the log file for details.")
    else:
        print("No threats were detected in the emails. All URLs are safe.")

    # Inform the user when the process is complete
    print("Email processing complete. Check the log file for details.")

if __name__ == "__main__":
    main()
