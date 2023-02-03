import requests
from bs4 import BeautifulSoup
import csv

# Initialize a list to store the data
data = []

# Loop through each URL
for url in product_urls:
    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract the information you need
    asin = soup.find("td", text="ASIN").find_next_sibling("td").text
    manufacturer = soup.find("td", text="Manufacturer").find_next_sibling("td").text
    description = soup.find("div", id="productDescription").text
    product_description = soup.find("div", id="feature-bullets").text
    
    # Store the extracted information as a dictionary
    product_data = {
        "Product URL": url,
        "ASIN": asin,
        "Manufacturer": manufacturer,
        "Description": description,
        "Product Description": product_description
    }

    # Append the product data to the data list
    data.append(product_data)

# Write the data to a CSV file
with open("product_data.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["Product URL", "ASIN", "Manufacturer", "Description", "Product Description"])
    writer.writeheader()
    for product_data in data:
        writer.writerow(product_data)
