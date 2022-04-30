#!/usr/bin/env python
# coding: utf-8

# In[1]:


#imports all the necessary libraries 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)


# In[2]:


#specify the path to chromedriver.exe (download and save on your computer)
driver = webdriver.Chrome('C:/Users/Dasun Gunasekara/chromedriver.exe', chrome_options=chrome_options)

#open the webpage
driver.get("http://www.facebook.com")


# In[3]:


#target username
username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']")))

#enter username and password
username.clear()
username.send_keys("my_username")
password.clear()
password.send_keys("my_password")

#target the login button and click it
button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

#We are logged in!

#wait 5 seconds to allow your new page to load
time.sleep(5)
images = [] 

#itterate over the page images
for i in ["photos_all", "photos_of"]:
    driver.get("https://www.facebook.com/MarinoBeachColombo/photos/?ref=page_internal" + i + "/")
    time.sleep(5)
    
    #scroll down
    #example: range(0,10) scrolls down 650+ images
    for j in range(0,1):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(10)

    #target all the link elements on the page
    anchors = driver.find_elements_by_tag_name('a')
    anchors = [a.get_attribute('href') for a in anchors]
    #narrow down all links to image links only
    anchors = [a for a in anchors if str(a).startswith("https://www.facebook.com/MarinoBeachColombo/photos/")]
    
    print('Found ' + str(len(anchors)) + ' links to images')
    
    #extract the [1]st image element in each link
    for a in anchors:
        driver.get(a) #navigate to link
        time.sleep(5) #wait a bit
        img = driver.find_elements_by_tag_name("img")
        for k in img:
            print(k.get_attribute("src"))
        images.append(img[1].get_attribute("src")) #may change in future to img[?]

print('I scraped '+ str(len(images)) + ' images!')


# In[4]:


images


# In[6]:


import os

path = os.getcwd()
path = os.path.join(path, "SCRAPED")

#create the directory
os.mkdir(path)
path


# In[7]:


import wget

#download images
counter = 0
for image in images:
    save_as = os.path.join(path, str(counter) + '.jpg')
    wget.download(image, save_as)
    counter += 1


# In[ ]:




