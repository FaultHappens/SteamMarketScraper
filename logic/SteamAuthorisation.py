from selenium import webdriver
from selenium.webdriver.common.by import By


steamAuthUrl = "https://steamcommunity.com/login/home/?goto="

def steamAuthorisation(driver: webdriver):
    steamLogin = input("Steam Login:\n")
    steamPass = input("Steam Password:\n")

    driver.get(steamAuthUrl)

    driver.find_element(By.NAME, "username").send_keys(steamLogin)
    driver.find_element(By.NAME, "password").send_keys(steamPass)
    driver.find_element(By.XPATH, "//button[@class='btn_blue_steamui btn_medium login_btn']").click()

    steamGuardCode = input("Steam Guard Code:\n")
    driver.find_element(By.ID, "twofactorcode_entry").send_keys(steamGuardCode)
    driver.find_element(By.XPATH, "//div[@class='auth_button leftbtn'][@type='submit']").click()
