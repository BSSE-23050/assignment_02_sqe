from selenium import webdriver 
driver = webdriver.Chrome() 
driver.get("https://edenrobe.com") 
print(driver.title) 
driver.quit() 