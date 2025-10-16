import re
import socket
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests
import whois
import urllib3
from datetime import datetime
import ssl

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Function to safely get the URL with error handling
def safe_get(url, timeout=10):
    try:
        response = requests.get(url, verify=False, timeout=timeout)
        return response
    except requests.exceptions.Timeout:
        print(f"Timeout occurred while trying to access: {url}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
    return None  # In case of error, return None

# Function to get the WHOIS information for a domain
def get_whois_info(domain):
    try:
        w = whois.whois(domain)
        creation_date = w.creation_date
        # Handle cases where creation_date is returned as a list or a single value
        if isinstance(creation_date, list):
            return creation_date[0] if creation_date else None
        return creation_date
    except Exception as e:
        print(f"Error fetching WHOIS info for {domain}: {e}")
        return None

# Function to check SSL certificate details
def check_ssl_certificate(domain):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                return cert is not None
    except Exception as e:
        print(f"Error checking SSL certificate for {domain}: {e}")
        return False

# Function to extract features from a URL based on the given attributes
def extract_features(url):
    features = {}

    # Step 1: Validate URL format
    try:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        if not domain:
            print(f"Invalid URL: {url}")
            return None
    except Exception as e:
        print(f"Error parsing URL {url}: {e}")
        return None

    # Step 2: Extract features
    try:
        features['having_IP_Address'] = 1 if bool(re.search(r'\d+\.\d+\.\d+\.\d+', url)) else -1
        features['URL_Length'] = 1 if len(url) < 54 else (0 if len(url) <= 75 else -1)
        features['Shortining_Service'] = 1 if any(service in url for service in ["bit.ly", "goo.gl", "tinyurl.com", "is.gd", "t.co", "ow.ly"]) else -1
        features['having_At_Symbol'] = 1 if '@' in url else -1
        features['double_slash_redirecting'] = 1 if '//' in url else -1
        features['Prefix_Suffix'] = 1 if url.startswith('www.') or url.endswith('.com') else -1
        features['having_Sub_Domain'] = 1 if len(parsed_url.netloc.split('.')) > 2 else 0
        features['SSLfinal_State'] = 1 if url.startswith('https') else (0 if 'https' not in url else -1)
    except Exception as e:
        print(f"Error extracting basic URL features for {url}: {e}")
        return None

    # Step 3: Fetch WHOIS data
    domain_creation_date = get_whois_info(domain)
    if domain_creation_date:
        current_year = datetime.now().year
        domain_creation_year = domain_creation_date.year if isinstance(domain_creation_date, datetime) else None
        if domain_creation_year:
            features['Domain_registeration_length'] = 1 if (current_year - domain_creation_year > 2) else -1
        else:
            features['Domain_registeration_length'] = -1
    else:
        features['Domain_registeration_length'] = -1

    # Step 4: Fetch page content using safe_get
    page = safe_get(url, timeout=10)  # Increased timeout to 10 seconds
    if page is None:
        print(f"Failed to fetch page content for {url}")
        return None  # If page fetch fails, return None

    # Step 5: Parse the HTML content
    try:
        soup = BeautifulSoup(page.text, 'html.parser')

        # Feature extraction from page content
        features['Favicon'] = 1 if soup.find('link', rel='icon') else -1
        features['port'] = 1 if ':' in parsed_url.netloc else -1
        features['HTTPS_token'] = 1 if 'https' in parsed_url.scheme else -1
        features['Request_URL'] = 1 if domain in str(soup.find_all('a')) else -1
        features['URL_of_Anchor'] = 1 if any(anchor.get('href') for anchor in soup.find_all('a')) else 0
        features['Links_in_tags'] = 1 if soup.find_all('a') else (0 if not soup.find_all('a') else 0)
        features['SFH'] = 1 if soup.find('form') else (0 if not soup.find('form') else 0)
        features['Submitting_to_email'] = 1 if 'mailto:' in str(soup.find_all('a')) else 0
        features['Abnormal_URL'] = 1 if bool(re.search(r'[^a-zA-Z0-9.-]', url)) else 0
        features['Redirect'] = 1 if any(meta.get('http-equiv') == 'refresh' for meta in soup.find_all('meta')) else 0
        features['on_mouseover'] = 1 if any('onmouseover' in str(tag.attrs) for tag in soup.find_all()) else 0
        features['RightClick'] = 1 if any('contextmenu' in str(tag.attrs) for tag in soup.find_all()) else 0
        features['popUpWidnow'] = 1 if any('popup' in str(tag.attrs) for tag in soup.find_all()) else 0
        features['Iframe'] = 1 if any('iframe' in str(tag.attrs) for tag in soup.find_all()) else 0

        # Suspicious keywords in page content
        # Check for robots.txt presence
        
    except Exception as e:
        print(f"Error parsing page content for {url}: {e}")
        return None

    # Step 6: Additional features (placeholders)
    features['age_of_domain'] = 1 if domain_creation_date else 0
    features['DNSRecord'] = 1 if bool(parsed_url.netloc) else 0
    features['web_traffic'] = 1  # Placeholder
    features['Page_Rank'] = 1    # Placeholder
    features['Google_Index'] = 1  # Placeholder
    features['Links_pointing_to_page'] = 1  # Placeholder
    features['Statistical_report'] = 1  # Placeholder

    return features

# Example usage
"""url = "http://google.com"
features = extract_features(url)
if features:
    print(features)
else:
    print("Feature extraction failed.")"""
