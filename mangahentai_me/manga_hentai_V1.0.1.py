from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import os
import requests
import io
import hashlib
from PIL import Image

opt = Options()
opt.add_argument("start-maximized")
opt.add_extension("/opt/google/chrome/AdBlock-—-best-ad-blocker.crx")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=opt)

def manga_henati(url):

    driver.get(url)

    manga_title = driver.find_element(By.TAG_NAME,"h1").text
    # print(manga_title)

    if not os.path.exists(manga_title):
        os.makedirs(manga_title)

    manga_chapter_container = driver.find_elements(By.XPATH,".//div[@class='listing-chapters_wrap cols-1  ']/ul/li/a")
    manga_chapters = []

    for chapters in manga_chapter_container:
        manga_chapters.append(chapters.text)
    # print(manga_chapters)

    def manga_download():

            manga_page = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT,manga)))
            manga_page.click()
            driver.implicitly_wait(1)

            manga_images = driver.find_elements(By.XPATH,"//div[@class='page-break no-gaps']/img")
            image_list = []

            for images in manga_images:
                if images.get_attribute("src") and "https" in images.get_attribute("src"):
                    image_link = images.get_attribute("src")
                    image_id = images.get_attribute("id")

                manga_chapter_title = driver.find_element(By.ID,"chapter-heading").text
                # print(manga_chapter_title)

                # if not os.path.exists(os.path.join(manga_title,manga_chapter_title)):
                #     os.makedirs(os.path.join(manga_title,manga_chapter_title))

                try:
                    image_content = requests.get(image_link).content
                except Exception as e:
                    print("Error on requesting image url",e)
                
                try:
                    image_byte = io.BytesIO(image_content)
                    image = Image.open(image_byte)
                    image_list.append(image)
                except Exception as e:
                    print(e)
                    
            print(f"The {manga_chapter_title} manga Download is Completed")

            file = os.path.join(manga_title,manga_chapter_title +".pdf")
            with open(file,"wb") as f:
                
                image_list[0].save(f,save_all=True,append_images=image_list[1:])

            driver.back()
            driver.implicitly_wait(1)

    for manga in manga_chapters:
        try:
            manga_download()
        
        except Exception as e:

            manga_page = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT,manga)))
            action = ActionChains(driver)
            action.move_to_element(manga_page).click().perform()
            driver.back()
            driver.implicitly_wait(1)

    
            manga_download()
    print(f"Download {manga_title} manga is Completed")

    driver.implicitly_wait(1)
    driver.quit()

