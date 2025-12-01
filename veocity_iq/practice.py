# import pandas as pd

# df = pd.read_csv("preprocessed_data.csv")

# # frequency of all unique values in a column
# print(df['Brand'].value_counts())

# df['your_column_name'] = pd.to_numeric(df['your_column_name'], errors='coerce')
# print(df['your_column_name'].sum())



# second scraping
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import time
# import pandas as pd 

# Car_name = []
# Brand = []
# Price = []
# Mileage = []
# Dealer = []

# driver = webdriver.Firefox()
# driver.set_window_size(1400, 900)

# brands = ["maserati", "mercedes-benz", "bugatti", "audi"]

# for brand in brands:
#     for page in range(1, 8):

#         url = f"https://www.dupontregistry.com/autos/results/{brand}/filter:page_start={page}"
#         driver.get(url)
#         time.sleep(4)

#         # CLOSE POPUP
#         close_btn = driver.find_elements(By.XPATH, "//button[@aria-label='Close']")
#         if close_btn:
#             close_btn[0].click()
#             time.sleep(1)

#         # SCROLL
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(2)

#         # BOX (XPATH ONLY)
#         box = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/main/div[3]/div/div[2]")

#         # CARDS
#         cards = box.find_elements(By.CLASS_NAME, "LilCards-module_product_item__O1t-R")

#         print(brand, "page", page, "cards:", len(cards))

#         for card in cards:
#             name = card.find_element(By.CLASS_NAME, "LilCards-module_title__Rnfg5").text
#             price = card.find_element(By.CLASS_NAME, "LilCards-module_product_price__CmGbR").text
#             mileage = card.find_element(By.CLASS_NAME, "LilCards-module_meta_text__sb2tE").text
#             dealer = card.find_element(By.CLASS_NAME, "LilCards-module_dealer_wrapper__AfDiA").text

#             Car_name.append(name)
#             Brand.append(brand)
#             Price.append(price)
#             Mileage.append(mileage)
#             Dealer.append(dealer)

# driver.quit()

# df = pd.DataFrame({
#     "Car Name": Car_name,
#     "Brand": Brand,
#     "Price": Price,
#     "Mileage": Mileage,
#     "Dealer": Dealer
# })

# df.to_csv("dataset2.csv", index=False)
# print("Scraping completed! total rows:", len(df))



# SCRAPING ALLL
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd 

Car_name = []
Brand = []
Price = []
Mileage = []
Dealer = []

driver = webdriver.Firefox()
driver.set_window_size(1400, 900)

brands = ["maserati", "mercedes-benz", "bugatti", "audi", "land--rover"]

for brand in brands:
    for page in range(1, 15):  # pages 1..14

        url = f"https://www.dupontregistry.com/autos/results/{brand}/filter:page_start={page}"
        driver.get(url)
        time.sleep(4)

        # CLOSE POPUP
        close_btn = driver.find_elements(By.XPATH, "//button[@aria-label='Close']")
        if close_btn:
            close_btn[0].click()
            time.sleep(1)

        # SCROLL
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        # BOX (XPATH ONLY)
        box = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/main/div[3]/div/div[2]")

        # CARDS
        cards = box.find_elements(By.CLASS_NAME, "LilCards-module_product_item__O1t-R")

        print(brand, "page", page, "cards:", len(cards))

        for card in cards:
            name = card.find_element(By.CLASS_NAME, "LilCards-module_title__Rnfg5").text
            price = card.find_element(By.CLASS_NAME, "LilCards-module_product_price__CmGbR").text
            mileage = card.find_element(By.CLASS_NAME, "LilCards-module_meta_text__sb2tE").text
            dealer = card.find_element(By.CLASS_NAME, "LilCards-module_dealer_wrapper__AfDiA").text

            Car_name.append(name)
            Brand.append(brand)
            Price.append(price)
            Mileage.append(mileage)
            Dealer.append(dealer)

driver.quit()

df = pd.DataFrame({
    "Car Name": Car_name,
    "Brand": Brand,
    "Price": Price,
    "Mileage": Mileage,
    "Dealer": Dealer
})

df.to_csv("dupont_supercars.csv", index=False)
print("Scraping completed! total rows:", len(df))
