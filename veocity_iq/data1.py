from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd 

Car_name = []
Price = []
Mileage = []
Dealer = []

driver = webdriver.Firefox()   # OPEN ONLY ONCE

for page in range(1, 8):
    url = f"https://www.dupontregistry.com/autos/results/maserati/filter:page_start={page}"
    driver.get(url)
    time.sleep(4)

    box = driver.find_element(By.XPATH, "/html/body/div[1]/main/div/div/div[2]/div")

    names = box.find_elements(By.CLASS_NAME, "item-title")
    for n in names:
        Car_name.append(n.text)

    prices = box.find_elements(By.CLASS_NAME, "item-price")
    for p in prices:
        Price.append(p.text)

    mileages = box.find_elements(By.CLASS_NAME, "item-mileage")
    for m in mileages:
        Mileage.append(m.text)

    dealers = box.find_elements(By.CLASS_NAME, "item-dealer")
    for d in dealers:
        Dealer.append(d.text)

# CLOSE DRIVER ONLY ONCE
driver.quit()

df = pd.DataFrame({
    "Car Name": Car_name,
    "Price": Price,
    "Mileage": Mileage,
    "Dealer": Dealer
})

df.to_csv("maserati_dupont.csv", index=False)
print("Scraping completed!")
