# One Piece Card Price Tracker

This project is a simple self‑hostable web application for tracking the prices of One Piece trading cards. Data is scraped from [TCGplayer](https://www.tcgplayer.com/) and stored in SQLite. A Flask API serves the data to a basic HTML interface that displays current prices and historical trends.

## Features

- Python scraper using `requests` and `BeautifulSoup` to fetch prices
- SQLite database to store cards and daily prices
- REST API built with Flask
- Responsive frontend with Bootstrap and Chart.js
- Searchable list of cards and historical price chart

## Requirements

- Python 3.8+

## Setup

1. **Clone and install dependencies**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. **Initialize the database and run the scraper**
   ```bash
   python scraper.py
   ```
   The scraper retrieves card information from TCGplayer and populates `cards.db`.
3. **Start the web application**
   ```bash
   python app.py
   ```
   Visit `http://localhost:5000` in your browser.

## Deployment Notes

The project is structured for easy migration to cloud hosting:

- Run the Flask app with Gunicorn for production: `gunicorn app:app`
- Serve static files with a web server such as Nginx
- SQLite can be replaced with another database like PostgreSQL when deploying to services such as AWS, Heroku, or Vercel.

## Legal

Scrape responsibly and respect TCGplayer’s terms of service. This project is for educational purposes.
