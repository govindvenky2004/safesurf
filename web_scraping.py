import requests
from bs4 import BeautifulSoup

def get_website_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup
    else:
        print("Failed to retrieve the website")
        return None

def extract_links(soup):
    links = []
    for link in soup.find_all('a', href=True):
        links.append(link['href'])
    return links

url = 'http://example.com'
soup = get_website_content(url)
if soup:
    links = extract_links(soup)
    print(links)
