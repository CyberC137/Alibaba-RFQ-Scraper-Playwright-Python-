# Alibaba RFQ Scraper (Playwright + Python)

This project scrapes **Request for Quotation (RFQ)** listings from [Alibaba's RFQ portal](https://sourcing.alibaba.com/rfq/rfq_search_list.htm) using Python and Playwright. It extracts structured buyer data and saves it in a clean CSV format.

---

##  Features

*  Scrapes **Title, Buyer Name, Country, Quantity, Quotes Left, Inquiry Time**
*  Detects buyer **flags** (Email Confirmed, Experienced Buyer, etc.)
*  Handles **pagination** (set how many pages to scrape)
*  Saves debug artifacts: screenshots and full DOM
*  Exports to `output.csv`

---

##  Requirements

* Python 3.7+
* pip

Install dependencies:

```bash
pip install playwright
pip install pandas
```

Install Playwright browser binaries:

```bash
playwright install
```

---

##  Usage

Run the scraper:

```bash
python scrape_alibaba_rfq.py
```

Set the number of pages to scrape by editing:

```python
MAX_PAGES = 3  # Change to scrape more pages
```

---

##  Output

* `output.csv` — cleaned, structured RFQ data
* `playwright_page_1.png`, `...` — page screenshots
* `debug_playwright_dom_1.html`, `...` — raw HTML for each page

---

##  Sample CSV Output

| Title             | Buyer Name   | Country              | Quotes Left | Quantity Required | Inquiry Time | Email Confirmed |
| ----------------- | ------------ | -------------------- | ----------- | ----------------- | ------------ | --------------- |
| Curve Monitor ... | PANDI SELVAM | United Arab Emirates | 8           | 1 Piece/Pieces    | 1 hour ago   | Yes             |

---

##  Legal Notice

This script is provided for educational and personal use only. Make sure your use complies with Alibaba’s [terms of service](https://rule.alibaba.com) and local data protection laws.

---

##  Credits

Built with [Playwright](https://playwright.dev/python/), [Pandas](https://pandas.pydata.org/), and regex magic 🪄.
