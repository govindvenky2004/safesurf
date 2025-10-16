import re
from urllib.parse import urlparse

def is_phishing(url):
    phishing_keywords = ['login', 'update', 'secure', 'verify', 'account', 'confirm']
    whitelisted_domains = ['canarabank.com', 'google.com']  # Add more as needed

    parsed_url = urlparse(url)
    
    # Check if the URL format is valid
    if not all([parsed_url.scheme, parsed_url.netloc]):
        print(f"Invalid URL format: {url}")
        return False

    # Exclude FTP URLs
    if parsed_url.scheme == 'ftp':
        return False

    # Check for localhost
    domain = parsed_url.netloc
    if domain in ['127.0.0.1', 'localhost']:
        return False

    # Check for whitelisted domains
    if domain in whitelisted_domains:
        return False

    # Check for common phishing keywords
    if any(keyword in url.lower() for keyword in phishing_keywords):
        print(f"Phishing keyword found in URL: {url}")
        return True

    # Check URL length, allow longer lengths with conditions
    if len(url) > 100:  # Change threshold as needed
        return True
    
    # Check for IP address in URL
    if any(char.isdigit() for char in domain):
        return True
    
    # Check for excessive special characters
    allowed_special_chars = r'[-_.~$]'
    special_chars = re.findall(r'[\W]', url)
    allowed_count = len(re.findall(allowed_special_chars, url))
    if len(special_chars) - allowed_count > 3:
        return True
    
    # Check for use of HTTPS
    if not url.startswith("https://"):
        print(f"Non-HTTPS URL detected: {url}")
        return True

    # Check for suspicious domain names
    suspicious_domains = ['example.com', 'phishingsite.com']
    if domain in suspicious_domains:
        return True
    
    # Check for subdomains
    if domain.count('.') > 2:
        return True
    
    # Check for redirection
    if "redirect" in url.lower():
        return True

    # Check if URL contains an email address
    if re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', url):
        return True
    
    return False
