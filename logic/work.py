from fileinput import hook_compressed
import inspect
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import json
from data.ItemInfo import ItemInfo
from typing import List
import time 


items: List[ItemInfo] = list()
alreadyChecked = []
maxPages = 1


def work(driver:webdriver, baseUrl:str, maxFloat: float):
    print("\n\n")
    mustReturn = False

    driver.get(baseUrl)
    try:
        nextPageBtn = driver.find_element(By.ID, "searchResults_btn_next")
    except:
        print("An exception occurred")
        return 
    for page in range(maxPages):
        print(f"Page #{page+1}:\n")
        nextPageBtn = driver.find_element(By.ID, "searchResults_btn_next")
        btns = driver.find_elements(By.CLASS_NAME, "market_actionmenu_button")
        for btn in btns:
            driver.execute_script("arguments[0].click();", btn)
            popup = driver.find_element(By.CSS_SELECTOR ,"#market_action_popup_itemactions > a")
            inspectLink = popup.get_attribute('href')
            if inspectLink not in alreadyChecked:
                checkFloat(inspectLink, maxFloat, driver)
        if(page+1 != maxPages):
            nextPageBtn.click()
            waitUntillNextPageLoads(page+2, driver)



    print("\n\n--------------------------------------------------------------------------------------")


def checkFloat(inspectLink: str, maxFloat: float, driver: webdriver):
    link = f"https://api.csgofloat.com/?url={inspectLink}"
    response = requests.get(link).text
    jsonResponse = json.loads(response)
    alreadyChecked.append(inspectLink)
    itemFloat = jsonResponse["iteminfo"]["floatvalue"]
    print(itemFloat)
    itemA = jsonResponse["iteminfo"]["a"]
    itemM = jsonResponse["iteminfo"]["m"]
    if(itemFloat <= float(maxFloat)):
        buyItem(itemM, itemA, driver)
        a = f"Got an item for ya!\n Float is {itemFloat}!\n {inspectLink}\n\n"
        print(a)
        with open('result.txt', 'a') as f:
            f.write(a)
        mustReturn = True



def waitUntillNextPageLoads(expectedPage: int, driver: webdriver):
    activePage = -1
    try:
        activePage = driver.find_element(By.XPATH, "//span[@class='market_paging_pagelink active']").text
    except:
        print("An exception occurred")
    i = 0
    while str(expectedPage) != activePage:
        if(i >= 100):
            i = 0
            driver.find_element(By.ID, "searchResults_btn_next").click()
        i += 1
        try:
            activePage = driver.find_element(By.XPATH, "//span[@class='market_paging_pagelink active']").text
        except:
            print("An exception occurred")
        time.sleep(0.1)

def buyItem(m: str, a:str, driver: webdriver):
    driver.execute_script(f"javascript:BuyMarketListing('listing', '{m}', 730, '2', '{a}')")
    buyBttn = driver.find_element(By.XPATH, "//a[@id='market_buynow_dialog_purchase'][@class='btn_green_white_innerfade btn_medium_wide btn_uppercase']")
    if buyBttn.text != "Add Funds":
        driver.find_element(By.XPATH, "//input[@type='checkbox'][@id='market_buynow_dialog_accept_ssa']").click()
        buyBttn.click()
        time.sleep(1)
        driver.find_element(By.XPATH, "//div[@class='newmodal_close with_label']")
    