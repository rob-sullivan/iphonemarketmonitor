from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import openpyxl
import re

# Configurable variables
BASE_URL = 'https://www.adverts.ie/for-sale/q_iPhone+14/'  # Replace with your actual website URL
PRODUCT_CONTAINER_CLASS = 'sr-grid-cell quick-peek-container'  # Class for the container of each product
DESCRIPTION_CLASS = 'title'  # Class for the product title/description
PRICE_CLASS = 'price'  # Class for the product price
NEXT_BUTTON_CLASS = 'next'  # Class for the "Next" button
DELAY_BETWEEN_REQUESTS = 5000  # Time delay (in seconds) between page requests
OUTPUT_FILE_NAME = 'iphone_data.xlsx'  # Name of the output Excel file

print("getting service")
# Automatically manage FirefoxDriver with the correct version
service = Service(executable_path='D:\Projects\repos\iphonemarketmonitor\geckodriver.exe')  # Update this to the actual path to geckodriver
driver = webdriver.Firefox(service=service)
print("going to: " + str(BASE_URL))
driver.get(BASE_URL)

# Initialize a list to store the data
iphone_data = []

# Scraping loop
while True:
    print("getting html")
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Find all product containers
    products = soup.find_all(class_=PRODUCT_CONTAINER_CLASS)
    
    for product in products:
        description = product.find(class_=DESCRIPTION_CLASS).get_text(strip=True)
        price_text = product.find(class_=PRICE_CLASS).get_text(strip=True)
        
        # Clean up the price text
        price_text = re.sub(r'[^\d.,]', '', price_text).replace(',', '.')
        print("got text: " + str(price_text))
        
        # Handle cases where there are multiple dots in the price
        if price_text.count('.') > 1:
            price_text = price_text.replace('.', '', price_text.count('.') - 1)
        
        try:
            price = float(price_text)
            iphone_data.append([description, price])
        except ValueError:
            print(f"Could not convert price: {price_text}")
            continue

    # Check for 'Next' button to navigate to the next page
    try:
        print("pressing next button")
        next_button_li = driver.find_element(By.CLASS_NAME, NEXT_BUTTON_CLASS)
        next_button = next_button_li.find_element(By.TAG_NAME, 'a')
        next_button.click()
        time.sleep(DELAY_BETWEEN_REQUESTS)  # Wait for the next page to load
    except Exception as e:
        print(f"Ending scrape: {e}")
        break  # Exit loop when no more pages are found or other exception occurs

driver.quit()

# Export to Excel using openpyxl
workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.title = "iPhone Data"

# Write headers
sheet.append(["Description", "Price"])

# Write data
for row in iphone_data:
    sheet.append(row)

# Save the file
workbook.save(OUTPUT_FILE_NAME)

print(f"Data has been scraped and saved to {OUTPUT_FILE_NAME}")
