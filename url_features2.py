import re
from urllib.parse import urlparse

def extract_url_features2(url):
    # Length of the URL
    url_length = len(url)
    
    # Check for the presence of 'https' (secure connection)
    is_https = 1 if url.startswith('https') else 0
    
    # Count the number of special characters
    special_char_count = len(re.findall(r'[@#\$\%\^&\*\(\)_\+!]', url))
    
    # Parse the URL to get domain features
    domain = urlparse(url).netloc
    domain_length = len(domain)
    
    # Example: Is the URL using a subdomain? (e.g., "sub.example.com")
    has_subdomain = 1 if len(domain.split('.')) > 2 else 0
    
    # Return the features as a list of numerical values
    return [url_length, is_https, special_char_count, domain_length, has_subdomain]
