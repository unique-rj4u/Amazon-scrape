import requests
import csv
from bs4 import BeautifulSoup

def scrape_amazon_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    results = soup.find_all("div", class_="s-result-item")
    products = []
    for result in results:
        product_url_element = result.find("a", class_="a-link-normal")
        if product_url_element is None:
            continue

        product_url = product_url_element["href"]
        product_name = result.find("span", class_="a-size-medium a-color-base a-text-normal")
        if product_name is None:
            continue
        product_price = result.find("span", class_="a-offscreen").text
        rating_element = result.find("span", class_="a-icon-alt")
        if rating_element is None:
            continue

        rating = rating_element.text.split(" ")[0]
        num_reviews_element = result.find("span", class_="a-size-base s-underline-text")
        if num_reviews_element is None:
            num_reviews = "0"
        else:
            num_reviews = num_reviews_element.text.strip().split(" ")[0]
        
        products.append({
            "product_url": product_url,
            "product_name": product_name,
            "product_price": product_price,
            "rating": rating,
            "num_reviews": num_reviews
        })
    return products

products = []
for i in range(1, 21):
    url = f"https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&page={i}&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"
    products += scrape_amazon_page(url)

with open("amazon_products.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["product_url", "product_name", "product_price", "rating", "num_reviews"])
    writer.writeheader()
    for product in products:
        writer.writerow(product)
