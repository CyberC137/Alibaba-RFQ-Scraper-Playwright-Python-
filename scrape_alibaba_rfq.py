import asyncio
import datetime
import re
import pandas as pd
from playwright.async_api import async_playwright

BASE_URL = "https://sourcing.alibaba.com/rfq/rfq_search_list.htm?country=AE&recently=Y&page={}"
MAX_PAGES = 3  # Change this to scrape more pages

async def scrape_rfq_page(page, page_number):
    url = BASE_URL.format(page_number)
    print(f"\nScraping page {page_number}...")
    await page.goto(url)
    await page.wait_for_timeout(6000)

    await page.screenshot(path=f"playwright_page_{page_number}.png", full_page=True)
    html = await page.content()
    #with open(f"debug_playwright_dom_{page_number}.html", "w", encoding="utf-8") as f:
        #f.write(html)

    cards = await page.query_selector_all("div:has-text('Quotes Left')")
    print(f"Found {len(cards)} RFQs on page {page_number}.")

    rfqs = []

    for card in cards:
        try:
            full_text = await card.inner_text()
            lines = [line.strip() for line in full_text.splitlines() if line.strip()]

            # Title and URL
            title_el = await card.query_selector("a")
            title = await title_el.inner_text() if title_el else ""
            href = await title_el.get_attribute("href") if title_el else ""
            inquiry_url = f"https://sourcing.alibaba.com{href}" if href and not href.startswith("http") else href

            # regex for structured values
            quantity_match = re.search(r"Quantity Required:\s*(\d[\d,]*)\s*(\w+/?\w*)", full_text)
            country_match = re.search(r"Posted in:\s*([^\n]+)", full_text)
            quotes_match = re.search(r"Quotes Left\s*(\d+)", full_text)
            date_match = re.search(r"Date Posted:\s*(.+?)\n", full_text)

            # Buyer name after posted date
            buyer_name = ""
            for i, line in enumerate(lines):
                if "Date Posted:" in line:
                    for j in range(i + 2, len(lines)):
                        possible = lines[j].strip()
                        if len(possible) > 1 and not re.match(r"^\W?$", possible):
                            buyer_name = possible
                            break
                    break

            # Flags by text detection
            flags = [line.lower() for line in lines if
                     "email confirmed" in line.lower()
                     or "experienced buyer" in line.lower()
                     or "complete order" in line.lower()
                     or "typically replies" in line.lower()
                     or "interactive user" in line.lower()]

            rfqs.append({
                "Title": title,
                "Buyer Name": buyer_name,
                "Country": country_match.group(1).strip() if country_match else "",
                "Quotes Left": quotes_match.group(1) if quotes_match else "",
                "Quantity Required": quantity_match.group(1) + " " + quantity_match.group(2) if quantity_match else "",
                "Inquiry Time": date_match.group(1).strip() if date_match else "",
                "Email Confirmed": "Yes" if any("email confirmed" in f for f in flags) else "No",
                "Experienced Buyer": "Yes" if any("experienced buyer" in f for f in flags) else "No",
                "Complete Order via RFQ": "Yes" if any("complete order" in f for f in flags) else "No",
                "Typical Replies": "Yes" if any("typically replies" in f for f in flags) else "No",
                "Interactive User": "Yes" if any("interactive user" in f for f in flags) else "No",
                "Inquiry URL": inquiry_url,
                "Scraping Date": datetime.datetime.now().strftime("%Y-%m-%d")
            })

        except Exception as e:
            print(f"Skipped one RFQ due to error: {e}")
            continue

    return rfqs

async def run():
    all_data = []
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=False, slow_mo=50)
        page = await browser.new_page()
        for i in range(1, MAX_PAGES + 1):
            try:
                data = await scrape_rfq_page(page, i)
                if not data:
                    print(f"No data found on page {i}. Stopping.")
                    break
                all_data.extend(data)
            except Exception as e:
                print(f" Failed to scrape page {i}: {e}")
                continue
        await browser.close()

    if not all_data:
        print(" No data scraped.")
        return

    df = pd.DataFrame(all_data)
    df.to_csv("output.csv", index=False)
    print(f"\n Scraped {len(df)} RFQs across {MAX_PAGES} pages. Saved to output.csv.")

if __name__ == "__main__":
    asyncio.run(run())
