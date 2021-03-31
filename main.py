# imports here
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import os
import time
import wget

# solution by pythonjar
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)

# specify the path to chromedriver.exe (download and save on your computer)
driver = webdriver.Chrome("chromedriver.exe", chrome_options=chrome_options)

# open the webpage
driver.get("http://www.facebook.com")

# target user and password
username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']")))

# enter username and password
username.clear()
username.send_keys("your email")
password.clear()
password.send_keys("your password")

# target the login button and click it
button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
time.sleep(5)

imgs_url = []  # 儲存照片連結

# get user facebook photo_of and photo_all url
for i in ["photo_of", "photo_all"]:
    driver.get("https://www.facebook.com/Blizzardsumme/" + i + "/")
    time.sleep(5)

    n_scrolls = 2
    for j in range(1, n_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

        anchors = driver.find_elements_by_tag_name("a")  # get 'a' tag
        anchors = [a.get_attribute("href") for a in anchors]  # get 'href' attributes in 'a' tag
        anchors = [a for a in anchors if str(a).startswith("https://www.facebook.com/photo")]  # find photo url store

        for a in anchors:
            driver.get(a)
            time.sleep(5)
            img = driver.find_elements_by_tag_name("img")
            imgs_url.append(img[0].get_attribute("src"))
            # for k in img:
            #     print(k.get_attribute("src"))

path = os.getcwd()  # 返回當前工作目錄
path = os.path.join(path, "ScrapePhotos")  # 儲存到這個資料夾內

# create the directory
os.mkdir(path)

counter = 0
for image in imgs_url:
    save_as = os.path.join(path, str(counter) + '.jpg')
    wget.download(image, save_as)  # 從網上下載資源，儲存在path資料夾內
    counter += 1
