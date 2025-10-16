from pymongo import MongoClient

# Create MongoDB client once and reuse it
client = MongoClient('mongodb://localhost:27017/')
db = client.SafeSurf
urls_collection = db.URLs
predictions_collection = db.predictions

def store_urls(urls):
    """Store a list of URLs in the database."""
    for url in urls:
        urls_collection.update_one({"url": url}, {"$setOnInsert": {"url": url}}, upsert=True)
    print(f"Stored {len(urls)} URLs in the database.")

def get_urls_from_db():
    """Retrieve URLs from the database."""
    # Fetch all documents and convert to a list of dictionaries (only the 'url' field)
    return list(urls_collection.find({}, {"_id": 0, "url": 1}))  # Only include the 'url' field

def store_predictions_in_db(urls, predictions):
    """Store predictions for the URLs in the database."""
    for url, prediction in zip(urls, predictions):
        record = {"url": url, "prediction": int(prediction)}  # Convert prediction to int if needed
        predictions_collection.update_one({"url": url}, {"$set": record}, upsert=True)  # Use upsert to update or insert
    print(f"Stored {len(urls)} predictions in the database.")
