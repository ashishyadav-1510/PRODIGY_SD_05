import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BASE_URL = 'https://books.toscrape.com/catalogue/page-{}.html'
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def fetch_page(page_number):
    try:
        url = BASE_URL.format(page_number)
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        books = soup.find_all('article', class_='product_pod')
        return [extract_book_info(book) for book in books if extract_book_info(book) is not None]
    except Exception as e:
        logging.error(f"Failed to fetch page {page_number}: {e}")
        return []

def extract_book_info(book):
    try:
        title = book.h3.a['title']
        price = book.find('p', class_='price_color').text
        availability = book.find('p', class_='instock availability').text.strip()
        rating_classes = book.p.get('class', [])
        rating = next((cls for cls in rating_classes if cls != 'star-rating'), 'Unknown')
        return {
            'Title': title,
            'Price': price,
            'Availability': availability,
            'Rating': rating
        }
    except Exception as e:
        logging.warning(f"Error extracting book data: {e}")
        return None

def scrape_books(start_page=1, end_page=3):
    all_books = []
    with ThreadPoolExecutor() as executor:
        results = executor.map(fetch_page, range(start_page, end_page))
        for page_books in results:
            all_books.extend(page_books)
    return all_books

def save_to_csv(book_list, filename='books.csv'):
    df = pd.DataFrame(book_list)
    df.to_csv(filename, index=False, encoding='utf-8')
    logging.info(f"Scraped {len(book_list)} books.")
    logging.info(f"Data saved to '{filename}'")

if __name__ == "__main__":
    books = scrape_books(start_page=1, end_page=3)  
    save_to_csv(books)