from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd 

Car_name = []
Price = []
Year = []
Mileage = []
Dealer = []

driver = webdriver.Firefox()   # OPEN ONLY ONCE

# Add the new brands here
brands = ["ferrari", "lamborghini", "porsche", "aston martin", "mercedes", "mclaren", "bentley"]

for brand in brands:
    for page in range(1, 9):
        url = f"https://www.supercartrader.com/products?search={brand}&page={page}"
        driver.get(url)
        time.sleep(4)

        box = driver.find_element(By.XPATH, "/html/body/div[4]/div/form/div[2]/div[2]/div[2]")

        # name
        names = box.find_elements(By.CLASS_NAME, "product-title")
        for n in names:
            Car_name.append(n.text)

        # dealer
        dealers = box.find_elements(By.CLASS_NAME, "product-user")
        for d in dealers:
            Dealer.append(d.text)

        # price | year | mileage
        details = box.find_elements(By.CLASS_NAME, "price")
        for det in details:
            info = det.text.split("|")
            Price.append(info[0].strip())
            Year.append(info[1].strip())
            Mileage.append(info[2].strip())

# CLOSE DRIVER ONLY ONCE
driver.quit()

# save csv
df = pd.DataFrame({
    "Car Name": Car_name,
    "Price": Price,
    "Year": Year,
    "Mileage": Mileage,
    "Dealer": Dealer
})

df.to_csv("all_brands_data.csv", index=False)
print("Scraping completed!")
