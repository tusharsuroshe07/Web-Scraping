import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# ---------------------------------
# CONFIG
# ---------------------------------
SEARCH_QUERY = "laptops"   # your keyword
PAGES_TO_SCRAPE = 5        # number of pages
BASE_URL = "https://www.flipkart.com/search?q=" + SEARCH_QUERY + "&page="

# ---------------------------------
# Storage for data
# ---------------------------------
data = {
    "Product Name": [],
    "Price": [],
    "Rating": [],
    "Product Link": []
}

# ---------------------------------
# Scraping Loop
# ---------------------------------
for page in range(1, PAGES_TO_SCRAPE + 1):
    url = BASE_URL + str(page)
    print(f"Scraping Page {page} → {url}")

    # Get HTML content
    response = requests.get(url, headers={
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.5"
    })

    soup = BeautifulSoup(response.text, "html.parser")

    # Main product cards
    products = soup.find_all("div", class_="_2kHMtA")

    for product in products:
        # Name
        name = product.find("div", class_="_4rR01T")
        name = name.text if name else "N/A"

        # Price
        price = product.find("div", class_="_30jeq3")
        price = price.text if price else "N/A"

        # Rating
        rating = product.find("div", class_="_3LWZlK")
        rating = rating.text if rating else "No Rating"

        # Product link
        link = product.a.get("href") if product.a else None
        link = "https://www.flipkart.com" + link if link else "N/A"

        # Store values
        data["Product Name"].append(name)
        data["Price"].append(price)
        data["Rating"].append(rating)
        data["Product Link"].append(link)

    time.sleep(1)  # polite scraping delay

# ---------------------------------
# Save to CSV
# ---------------------------------
df = pd.DataFrame(data)
df.to_csv("flipkart_bs_products.csv", index=False)

print("\nScraping Completed!")
print("Data saved as → flipkart_bs_products.csv")
