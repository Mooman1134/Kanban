"""Scrapes One Piece card prices from TCGplayer."""
import time
import requests
from bs4 import BeautifulSoup
import database

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; CardPriceTracker/1.0)"
}

SEARCH_URL = (
    "https://www.tcgplayer.com/search/one-piece-card-game/product?page={page}"
)


def parse_page(html):
    soup = BeautifulSoup(html, "html.parser")
    listings = soup.select(".search-result__product")
    for item in listings:
        name_tag = item.select_one(".search-result__product-name")
        set_tag = item.select_one(".search-result__product-set")
        price_tag = item.select_one(".search-result__market-price")
        if not (name_tag and set_tag and price_tag):
            continue
        name = name_tag.get_text(strip=True)
        set_name = set_tag.get_text(strip=True)
        price_text = price_tag.get_text(strip=True).replace("$", "")
        try:
            price = float(price_text)
        except ValueError:
            continue
        card_id = database.get_or_create_card(name, set_name)
        database.add_price(card_id, price)
        print(f"Saved {name} - {set_name}: ${price:.2f}")


def scrape(max_pages=1):
    for page in range(1, max_pages + 1):
        url = SEARCH_URL.format(page=page)
        resp = requests.get(url, headers=HEADERS)
        if resp.status_code != 200:
            print("Failed to fetch page", page)
            break
        parse_page(resp.text)
        time.sleep(3)


if __name__ == "__main__":
    database.init_db()
    scrape(max_pages=5)
