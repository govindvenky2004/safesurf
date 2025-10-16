import requests
from pymongo import MongoClient, errors

# Step 1: Connect to MongoDB
def create_mongo_client():
    try:
        # If using MongoDB Atlas, replace with your Atlas URI
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)  # Timeout to detect connection issues
        db = client["url"]  # Create or connect to a database
        collection = db["url"]  # Create or connect to a collection
        # Ensure the connection is valid
        client.server_info()
        return collection
    except errors.ServerSelectionTimeoutError as e:
        print(f"Error: Unable to connect to MongoDB - {e}")
        return None

# Step 2: Fetch phishing URLs from OpenPhish feed
def fetch_openphish_urls():
    try:
        url = 'https://www.openphish.com/feed.txt'
        response = requests.get(url, timeout=10)  # Add a timeout to prevent indefinite waits
        response.raise_for_status()  # Raise an HTTPError for bad responses
        phishing_urls = response.text.splitlines()  # Each line contains one URL
        return phishing_urls
    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to fetch OpenPhish URLs - {e}")
        return []

# Step 3: Store the URLs in MongoDB
def store_urls_in_mongo(urls, collection):
    if not collection:
        print("Error: No MongoDB collection to store data.")
        return
    inserted_count = 0
    for url in urls:
        try:
            # Each document contains a URL and a prediction (0 for phishing)
            document = {
                "url": url,
                "prediction": 0  # 0 indicates phishing
            }
            collection.insert_one(document)  # Insert the document into the collection
            inserted_count += 1
        except errors.PyMongoError as e:
            print(f"Error: Failed to insert URL {url} into MongoDB - {e}")
    print(f"Stored {inserted_count}/{len(urls)} phishing URLs in MongoDB.")

# Step 4: Main function to scrape and store data
def main():
    collection = create_mongo_client()  # Connect to MongoDB collection
    if collection:
        phishing_urls = fetch_openphish_urls()  # Fetch phishing URLs from OpenPhish
        if phishing_urls:
            store_urls_in_mongo(phishing_urls, collection)  # Store URLs in MongoDB
        else:
            print("No URLs fetched from OpenPhish.")

if __name__ == '__main__':
    main()
