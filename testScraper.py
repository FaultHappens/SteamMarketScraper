from fileinput import hook_compressed
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import json
from data.ItemInfo import ItemInfo
from logic.SteamAuthorisation import steamAuthorisation
from logic.work import work
import time 

driver = webdriver.Chrome(executable_path="C:\\SteamMarketScraper\\chromedriver.exe")

steamAuthorisation(driver)

items = []

baseUrl = input("Type the url of item you want to observe?\n")
maxFloat = input("Whats the max float value you want to buy?\n")
baseUrl += "?query=&start=0&count=100"
while True:
    work(driver, baseUrl, maxFloat)
    time.sleep(2)




