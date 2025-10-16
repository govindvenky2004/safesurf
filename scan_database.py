from pymongo import MongoClient
from datetime import datetime

# Set up MongoDB connection
client = MongoClient('mongodb://localhost:27017/')  # Adjust the connection string if necessary
db = client['safesurf']  # Connect to the 'safesurf' database
scans_collection = db['scans']  # Access the 'scans' collection

# Function to store scan result in MongoDB
def store_scan_result(scan_type, scan_value, is_phishing):
    # Create a dictionary to represent the scan record
    scan_record = {
        'scan_type': scan_type,        # Type of scan (URL or Email)
        'scan_value': scan_value,      # The scanned value (URL or email)
        'is_phishing': is_phishing,    # Whether the scan value is phishing
        'timestamp': datetime.now()    # Current timestamp
    }

    # Insert the record into the database
    scans_collection.insert_one(scan_record)
    print(f"Scan result stored: {scan_record}")

# Example usage of storing scan results
def scan_url(url):
    # Perform phishing detection (this is just a placeholder for your detection logic)
    is_phishing = phishing_detection_logic(url)  # Replace with your actual detection logic

    # Store result in database
    store_scan_result('URL', url, is_phishing)

def scan_email(email):
    # Perform phishing detection (this is just a placeholder for your detection logic)
    is_phishing = phishing_detection_logic(email)  # Replace with your actual detection logic

    # Store result in database
    store_scan_result('Email', email, is_phishing)

# Example functions that would be part of your scan logic
def phishing_detection_logic(value):
    # Placeholder logic for phishing detection (you can integrate your ML model here)
    # For demonstration, let's assume URLs or emails containing "phishing" are phishing
    if 'phishing' in value:
        return True
    else:
        return False

# Example: Scanning a URL and storing the result
scan_url("http://example.com/phishing-url")

# Example: Scanning an email and storing the result
scan_email("suspicious@example.com")
