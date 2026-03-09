import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = "https://books.toscrape.com/catalogue/page-{}.html"

data = []

for page in range(1, 6):  # scrape first 5 pages
    url = base_url.format(page)

    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    books = soup.find_all("article", class_="product_pod")

    for book in books:
        title = book.h3.a["title"]
        price = book.find("p", class_="price_color").text.strip().replace("Â", "")
        rating = book.find("p", class_="star-rating")["class"][1]

        data.append({
            "Title": title,
            "Price": price,
            "Rating": rating,
            "Page": page
        })

df = pd.DataFrame(data)
df.to_csv("books_data.csv", index=False)

print(df.head())
print(f"\nScraped {len(df)} books")