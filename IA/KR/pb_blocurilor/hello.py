from bs4 import BeautifulSoup
import requests
import re
import locationtagger

from urllib.parse import urljoin
import nltk
import spacy

# essential entity models downloads
def download():
    nltk.downloader.download('maxent_ne_chunker')
    nltk.downloader.download('words')
    nltk.downloader.download('treebank')
    nltk.downloader.download('maxent_treebank_pos_tagger')
    nltk.downloader.download('punkt')
    nltk.download('averaged_perceptron_tagger')

""" 


def scrape_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a')
    return links

def extract_addresses_from_links(links, base_url):
    addresses = []
    for link in links:
        url = urljoin(base_url, link['href'])
        soup = scrape_website(url)
        address = extract_address(soup)
        addresses.append(address)
    return addresses
"""
def extract_address(soup):
    # This is a simple example using regex and it might not work for all websites
    #address = re.findall(r'\d{1,4} [\w\s]{1,20}(?:street|st|avenue|ave|road|rd|highway|hwy|square|sq|location)[\w\s]{1,20}, [\w\s]{1,20}, \w{2} \d{5}', soup.text, re.IGNORECASE)
    #address = re.findall(r'Location:\s*.+', soup.text, re.DOTALL)
    #address = re.findall(r'location', soup.text, re.IGNORECASE)
    #
    return []


sample_text = "India has very rich and vivid culture\
           widely spread from Kerala to Nagaland to Haryana to Maharashtra. " \
                  "Delhi being capital with Mumbai financial capital.\
                  Can be said better than some western cities such as " \
                  " Munich, London etc. Pakistan and Bangladesh share its borders"
#print(sample_text)
place_entity = locationtagger.find_locations(text=sample_text)
# getting all country regions
print("The countries regions in text : ")
print(place_entity.country_regions)

# getting all country cities
print("The countries cities in text : ")
print(place_entity.country_cities)


def crawl_website(base_url):
    visited = set()
    to_visit = [base_url]
    addresses = []

    while to_visit:
        current_url = to_visit.pop(0)
        visited.add(current_url)
        response = requests.get(current_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        address = extract_address(soup)
        addresses.append(address)
        links = soup.find_all('a')
        for link in links:
            url = urljoin(base_url, link.get('href', ''))
            if url not in visited and base_url in url:
                to_visit.append(url)

    print("FOR ", base_url, " we visited: ", visited)
    return addresses

k = 3


print("x = " , k)


domains = ['https://www.namastereiki.com/', 'https://hugsforhealing.org/', 'https://www.bentsoninsurance.net/']

"""for domain in domains:
    print(crawl_website(domain))
response = requests.get(domains[0])
soup = BeautifulSoup(response.text, 'html.parser')
links = soup.find_all('a')
print(links)"""

#print(crawl_website(domains[0]))