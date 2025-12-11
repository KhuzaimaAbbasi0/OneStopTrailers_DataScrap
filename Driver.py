import csv
import time
from urllib.parse import urljoin
from seleniumbase import Driver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
driver = Driver(uc=True)
base_url="https://www.onestoptrailershop.com/search/inventory"


fieldnames = ["URL", "Title", "Price", "Sale", "Saving"]
all_data = []
PDP_URLs=[]
All_PLPs=[]
All_PDPs=[]
# Step 1: Extract URLs and PLP-only data
driver.uc_open_with_reconnect(base_url, reconnect_time=4)
time.sleep(10)
while True:
   
    product_cards = driver.find_elements("css selector",".search-result")   #Get All Trailers
    

    for card in product_cards: #Through each trailer

        href_elem = card.find_element("css selector", ".results-heading a")
        href= href_elem.get_attribute("href")  #Get Link to PDP
     
        if href:
            plp_data ={}
            plp_data["URL"]=href, PDP_URLs.append(href)
            Heading_text=""
            Heading=card.find_elements("css selector",".results-heading span")
            for X in Heading:
                 Heading_text= Heading_text+X.text.strip()
            plp_data["Title"]=Heading_text
            plp_data["Price"]=card.find_element("css selector",".price-section span").text.strip()
            try:
                Sales_State=card.find_element("css selector", ".on-sale-label")
                plp_data["Sale"]=True
                Saving=card.find_element("css selector", ".sale-regular-price").text.strip()
                plp_data['Saving']=Saving
            except:
                 plp_data["Sale"]=False
                 plp_data['Saving']=""
            Table=card.find_element("css selector",".search-results-attributes")
            Td_Titles=Table.find_elements("tag name", "strong")
            Td_Values=Table.find_elements("css selector", "td[class]")
                
            for Titles,Values in zip(Td_Titles,Td_Values):
                TitleText=Titles.text.strip().lower()
                if TitleText not in fieldnames:
                    fieldnames.append(TitleText)
                plp_data[TitleText]=Values.text.strip()
        All_PLPs.append(plp_data)
        with open("trailers.csv", "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(All_PLPs)


    try:
        next_element=driver.find_element("css selector","a[aria-label='Next']")
        next_url=next_element.get_attribute("href")
        driver.get(next_url)

    except:
         break
    


    
    
                
         


    
      

# while True:
#         i=0
#         for Page in PDP_URLs:
#             human_sleep()
#             # wait_for_manual_captcha(driver)        
#             driver.get(Page)
           
#             All_PDPs.append(pdp_data)
            
            
        
#         for plp, pdp in zip(All_PLPs, All_PDPs):
#             new_data = {**plp, **pdp}
#             all_data.append(new_data)
              