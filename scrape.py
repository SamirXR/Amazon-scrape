import csv
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# Set up Chrome options for Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("window-size=1920,1080")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")

# Initialize the WebDriver with ChromeDriverManager and options
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL to scrape
url = "https://www.amazon.in/s?rh=n%3A6612025031&fs=true&ref=lp_6612025031_sar"

# Generate a random filename
filename = f"amazon_products_{random.randint(1000,9999)}.csv"

try:
    # Load the page with a timeout
    driver.get(url)
    driver.set_page_load_timeout(10)
    time.sleep(3)  # Wait to ensure the page has loaded

    # Get the page source and parse it with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    products = soup.find_all('div', {'data-component-type': 's-search-result'})

    # Open a CSV file to save the data
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(["Product Name", "Price", "Rating", "Seller", "Bought Last Month"])

        # Loop through each product and extract data
        for product in products:
            # Extract Product Name
            name_tag = product.find('a', class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')
            product_name = name_tag.text.strip() if name_tag else "N/A"
            
            # Extract Price
            price_tag = product.find('span', class_='a-price-whole')
            price = price_tag.text.strip() if price_tag else "N/A"
            
            # Extract Rating
            rating_tag = product.find('span', class_='a-icon-alt')
            rating = rating_tag.text.strip() if rating_tag else "N/A"
            
            # Extract Seller Name
            seller_tag = product.find('span', class_='a-size-small a-color-base')
            seller_name = seller_tag.text.strip() if seller_tag else "N/A"
            
            # Extract "Bought Last Month" information
            store_name_tag = product.find('span', class_='a-size-base a-color-secondary')
            bought_last_month = store_name_tag.text.strip() if store_name_tag else "N/A"

            # Write the row to the CSV file
            writer.writerow([product_name, price, rating, seller_name, bought_last_month])

    print(f"CSV file '{filename}' saved.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the Selenium browser
    driver.quit()
