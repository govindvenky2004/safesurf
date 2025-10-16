import imaplib
import logging

# Setup logging for better error tracking
logging.basicConfig(level=logging.INFO)

def list_imap_folders(imap):
    # Get all folder names (labels in Gmail)
    status, folders = imap.list()
    if status == "OK":
        folder_names = [folder.decode().split(' "/" ')[-1] for folder in folders]
        return folder_names
    else:
        logging.error("Failed to retrieve folders.")
        return []

def list_email_folders(email_address, password):
    try:
        # Connect to the Gmail IMAP server
        imap = imaplib.IMAP4_SSL("imap.gmail.com")
        imap.login(email_address, password)
        
        # List all available folders
        available_folders = list_imap_folders(imap)
        logging.info(f"Available folders: {available_folders}")
        
        # Logout after operation
        imap.logout()
        
        return available_folders

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return []

# Example usage
email_address = "govindvenkatesh2004@gmail.com"
password = "cdzz azfs ewba huqp"

folders = list_email_folders(email_address, password)
print(f"Available Folders: {folders}")
