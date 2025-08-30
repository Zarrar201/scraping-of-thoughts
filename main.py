import requests
from bs4 import BeautifulSoup
class QuoteScraper:
    
    """A scraper to fetch quotes and authors from quotes.toscrape.com"""
    BASE_URL = "https://quotes.toscrape.com/page/{}/"
    def __init__(self, pages_to_scrape, output_file):
        self.pages_to_scrape = pages_to_scrape
        self.output_file = output_file
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/129.0.0.0 Safari/537.36"
            )
        }
    def fetch_page(self, url):
        """Download HTML content from a given URL."""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def parse_quotes(self, html_content):
        """Extract quotes and authors from HTML page."""
        soup = BeautifulSoup(html_content, "lxml")
        for quote, author in zip(
            soup.select("span.text"),
            soup.select("small.author")
        ):
            yield quote.text.strip(), author.text.strip()

    def save_quotes(self, quotes):
        """Save quotes and authors to file."""
        with open(self.output_file, "a", encoding="utf-8") as f:
            for quote, author in quotes:
                f.write(f"{quote}\n- {author}\n\n")

    def run(self):
        """Scrape multiple pages and save results."""
        for page in range(1, self.pages_to_scrape + 1):
            url = self.BASE_URL.format(page)
            print(f"Scraping page {page} -> {url}")
            html = self.fetch_page(url)
            if html:
                quotes = self.parse_quotes(html)
                self.save_quotes(quotes)
        print(f"\n✅ Quotes saved to {self.output_file}")


def main():
    while True:
        try:
            pages = int(input("Enter number of pages to scrape: "))
            break
        except ValueError:
            print("Please enter a valid number.")

    file_name = input("Enter output file name (without extension): ") + ".txt"

    scraper = QuoteScraper(pages_to_scrape=pages, output_file=file_name)
    scraper.run()


if __name__ == "__main__":
    main()
