from pymongo import MongoClient
from datetime import datetime

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')  # Replace with your MongoDB connection string
db = client['SafeSurfDB']  # Replace with your database name

# Collections
url_logs_collection = db['url_predictions']  # Replace with your collection name
email_logs_collection = db['email_Data']  # Replace with your collection name

# Fetch recent URL logs (assuming there's a 'timestamp' field)
recent_url_logs = list(url_logs_collection.find({}).sort('timestamp', -1).limit(5))  # Fetch last 5 entries
recent_email_logs = list(email_logs_collection.find({}).sort('timestamp', -1).limit(5))  # Fetch last 5 entries

# Print the results
print("Recent URL Logs:")
for log in recent_url_logs:
    print(log)

print("\nRecent Email Logs:")
for log in recent_email_logs:
    print(log)
