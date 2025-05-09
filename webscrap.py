
import requests
from bs4 import BeautifulSoup
import re

def scrape_and_clean(url):
    """
    Scrapes and cleans visible text from a given URL.
    
    Args:
        url (str): The URL of the webpage to scrape.
        
    Returns:
        str: Cleaned visible text from the webpage.
    """
    # Fetch page content
    response = requests.get(url)
    html_content = response.content

    # Parse HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # Remove unnecessary tags
    for script in soup(["script", "style"]):
        script.extract()

    # Get all visible text
    text = soup.get_text(separator=' ', strip=True)

    # Clean excessive whitespaces
    clean_text = re.sub(r'\s+', ' ', text)

    return clean_text


#print(scrape_and_clean("https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"))