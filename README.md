# Books to Scrape - Web Scraper

A powerful and efficient Python web scraper that collects book information like  **title** ,  **price** ,  **availability** , and **rating** from [BooksToScrape.com](https://books.toscrape.com/). It uses **multithreading** for faster scraping and stores the data into a structured CSV file.

## Features

* Extracts  **Title** ,  **Price** ,  **Availability** , and **Rating** of each book
* Scrapes multiple pages concurrently using `ThreadPoolExecutor`
* Cleans and stores data in a well-formatted CSV file
* Error handling with logging for failed pages or data
* Beginner-friendly code and modular structure

## How It Works

### 1. Fetching Web Pages

The function `fetch_page(page_number)` dynamically constructs the URL for each catalog page like:

https://books.toscrape.com/catalogue/page-1.html

Then uses `requests.get()` with a user-agent header to fetch the HTML.

url = BASE_URL.format(page_number)
response = requests.get(url, headers=HEADERS, timeout=10)

It parses the page using BeautifulSoup and finds all books using:

books = soup.find_all('article', class_='product_pod')

### 2. Extracting Book Info

Each book is parsed to extract:

* **Title** : from the `<a>` tag inside `<h3>`
* **Price** : using the class `price_color`
* **Availability** : using the class `instock availability`
* **Rating** : extracted from the class names like `star-rating Three`

def extract_book_info(book):
    title = book.h3.a['title']
    price = book.find('p', class_='price_color').text
    availability = book.find('p', class_='instock availability').text.strip()
    rating_classes = book.p.get('class', [])
    rating = next((cls for cls in rating_classes if cls != 'star-rating'), 'Unknown')

### 3. Concurrent Page Scraping

The `scrape_books()` function uses `ThreadPoolExecutor` to scrape multiple pages at once:

with ThreadPoolExecutor() as executor:
    results = executor.map(fetch_page, range(start_page, end_page))

Each result is a list of dictionaries representing books, which are combined.

### 4. Saving Data to CSV

Finally, all data is written to a CSV file using pandas:

df = pd.DataFrame(book_list)
df.to_csv(filename, index=False, encoding='utf-8')

## Output Format

The CSV file (`books.csv`) will look like this:

| Title              | Price   | Availability | Rating |
| ------------------ | ------- | ------------ | ------ |
| A Light in the ... | £51.77 | In stock     | Three  |
| Tipping the Velvet | £53.74 | In stock     | One    |
| Soumission         | £50.10 | In stock     | One    |

## Sample Code Snippet

if __name__ == "__main__":
    books = scrape_books(start_page=1, end_page=3)
    save_to_csv(books)

Change `start_page` and `end_page` as needed to scrape more or fewer pages.

## Screenshots
### Code:

![image](https://github.com/ashishyadav-1510/PRODIGY_SD_05/blob/main/screenshot/Screenshot%202025-07-15%20170917.png?raw=true)

### Output:

![image](https://github.com/ashishyadav-1510/PRODIGY_SD_05/blob/main/screenshot/Screenshot%202025-07-15%20170948.png?raw=true)

### Scraped Data in CSV

![image](https://github.com/ashishyadav-1510/PRODIGY_SD_05/blob/main/screenshot/Screenshot%202025-07-15%20171048.png?raw=true)
![image](https://github.com/ashishyadav-1510/PRODIGY_SD_05/blob/main/screenshot/Screenshot%202025-07-15%20171137.png?raw=true)

## Video

[Video on YouTube](https://youtu.be/FGxdfQ6YLVk)

## Explaination

🔧 1. Imports – Bringing in Tools
import requests
Imports the requests library, used to send HTTP requests to websites and fetch their HTML content.

from bs4 import BeautifulSoup
Imports BeautifulSoup from bs4, used for parsing and navigating HTML content easily.

import pandas as pd
Imports pandas, a powerful library to handle tabular data (used here to save book data to CSV).

import logging
Imports Python’s built-in logging module to keep track of errors and events during execution.

from concurrent.futures import ThreadPoolExecutor
Imports ThreadPoolExecutor, which allows concurrent execution of function calls to speed up the scraping of multiple pages.

🛠️ 2. Logging Configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
Configures the logger to:

Show log messages of INFO level or higher (like ERROR, WARNING)

Use a format: timestamp – log level – message

🌐 3. Global Variables
BASE_URL = 'https://books.toscrape.com/catalogue/page-{}.html'
A URL template where {} will be replaced with the page number during scraping.

HEADERS = {'User-Agent': 'Mozilla/5.0'}
A header to simulate a real browser request. Some sites block scripts without a User-Agent.

📄 4. Fetching a Page
def fetch_page(page_number):
A function that downloads a single page of books.

    try:
        url = BASE_URL.format(page_number)
Replaces {} in BASE_URL with the actual page number to get the full URL.

        response = requests.get(url, headers=HEADERS, timeout=10)
Sends a GET request to the URL with browser headers and a timeout of 10 seconds.

        response.raise_for_status()
If the request fails (e.g., 404 or 500), it raises an error and skips processing.

        soup = BeautifulSoup(response.text, 'html.parser')
Parses the HTML response using BeautifulSoup.

        books = soup.find_all('article', class_='product_pod')
Finds all <article> tags with class product_pod — each one represents a book.

        return [extract_book_info(book) for book in books if extract_book_info(book) is not None]
Calls extract_book_info() on each book to extract its details.

Skips books that return None (e.g., due to errors during extraction).

    except Exception as e:
        logging.error(f"Failed to fetch page {page_number}: {e}")
        return []
Catches any error during fetching and logs an error message.

Returns an empty list if the page fails to load.

📚 5. Extracting Book Info
def extract_book_info(book):
A helper function that extracts data from a single book.

    try:
        title = book.h3.a['title']
Extracts the title from the <a> tag inside <h3>.

        price = book.find('p', class_='price_color').text
Finds the <p> tag with class price_color and gets its text (like '£51.77').

        availability = book.find('p', class_='instock availability').text.strip()
Gets the text from the availability tag and removes extra whitespace.

        rating_classes = book.p.get('class', [])
Gets the list of classes of the first <p> tag. One of them indicates the star rating (e.g., ["star-rating", "Three"]).

        rating = next((cls for cls in rating_classes if cls != 'star-rating'), 'Unknown')
From the list of classes, selects the one that's not 'star-rating' — this is the actual rating (e.g., Three).

        return {
            'Title': title,
            'Price': price,
            'Availability': availability,
            'Rating': rating
        }
Returns a dictionary containing the extracted data.

    except Exception as e:
        logging.warning(f"Error extracting book data: {e}")
        return None
If extraction fails, logs a warning and returns None.

🔄 6. Scraping Multiple Pages
def scrape_books(start_page=1, end_page=3):
Scrapes multiple pages — default: page 1 to page 2 (since range(start, end) excludes end).

    all_books = []
Initializes an empty list to hold all books.

    with ThreadPoolExecutor() as executor:
Creates a thread pool to run tasks concurrently (faster scraping).

        results = executor.map(fetch_page, range(start_page, end_page))
Uses executor.map() to call fetch_page() for each page in the range.

        for page_books in results:
            all_books.extend(page_books)
Appends all books from each page to the main list.

    return all_books
Returns the complete list of books.

💾 7. Saving to CSV
def save_to_csv(book_list, filename='books.csv'):
Saves the list of books to a CSV file.

    df = pd.DataFrame(book_list)
Converts the list of dictionaries to a DataFrame (like a table).

    df.to_csv(filename, index=False, encoding='utf-8')
Writes the DataFrame to a CSV file without row indices.

    logging.info(f"Scraped {len(book_list)} books.")
    logging.info(f"Data saved to '{filename}'")
Logs the total number of books scraped and confirms CSV save.

🚀 8. Entry Point
if __name__ == "__main__":
This ensures the below block runs only when this file is executed directly, not when imported as a module.

    books = scrape_books(start_page=1, end_page=3)
Scrapes books from page 1 and 2 (end_page=3 is excluded in range).

    save_to_csv(books)
Saves the scraped book list to books.csv.

## Author
***Ashish Yadav***