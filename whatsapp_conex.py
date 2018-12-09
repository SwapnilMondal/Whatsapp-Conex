## This is a Whatsapp Contact Extractor or in short Whatsapp Conex.
## This is done using selenium to automate the work

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import glob
from requests import get
#from bs4 import BeautifulSoup
import os, time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import openpyxl, sys, glob

# This from_file contains group's names to use for searching or extracting. Type the name of the groups in from_file.txt
from_file = open('from_file.txt', 'r+')
to_file = open('contact_file.txt', 'a+')         # file to which the contacts are to be saved

groups = []
group_name = from_file.read().split('\n')
    
print("Groups from which the contacts are supposed to be extracted from: ")
print(group_name)

column = 1

chromedriver = "C:\Python27"
os.environ["webdriver.chrome.driver"] = chromedriver

url = "https://web.whatsapp.com/"

driver = webdriver.Chrome()

#wait = WebDriverWait(driver, 5)
driver.get(url)
response = get(url)
#print(response.text)
## this time gives the page some time to load or else sometimes the code don't work or skips
time.sleep(10)                   

print("Your web whatsapp is open ...\n ")
for target in group_name:
    try:
        driver.maximize_window()
                                  # search tab is selected 
        elem = driver.find_element_by_tag_name('label').send_keys(target)
        time.sleep(1)
    # clicking the closest searched element i.e. _2wP_Y
        x_arg = "_2wP_Y"
        location_list = []

# This part is specifically made to count the element's distance so that it could be used
# you can use this to locate the style of the chats by passing the xpath along with style using By.xpath and style 
        group_title = driver.find_element_by_class_name(x_arg)
        for i in range(50):
            location = group_title.location
            location_list.append(location)
            i = i+1
 
# Clicking the matched group       
        group_title.click()
        time.sleep(3)

    ## from here the names are taken for that click
    ## O90ur is the main class element through which it's extracting the contacts since all groups have this common class
        group_values = driver.find_element_by_class_name('O90ur')
        group_values.click()
        time.sleep(3)
        group_num_str = group_values.text
        u_contact_list = group_num_str.split(',')
        #print u_contact_list
        time.sleep(5)
        
 ##############################################################################################################################

# building and segregating the contacts
        contacts = []
        contact_list = []
        def check():
                
            print("Your numbers are being processed ... \n")
            for i in u_contact_list:
                unicode_key = i.encode('ascii')                # to remove the u' which is extracted along with the contacts
                contacts.append(unicode_key)

 ## This part may need some changes if you want to extract just the numbers and not the saved names
## if you write something let me know
            for i in contacts:
                if i.isalnum() == False:
                    try:
                        contact_list.append(int(i))
                        print("%s already exists in your contacts."%i)
                    except ValueError:
                        contact_list.append(i)
                else:
                    contact_list.append(i)
                
            #print contact_list
  # To save the extracted contacts into the target contact_file.txt
        def concatenate(contact_list):
            for i in contact_list:
                temp = i.split()
                contact_list.pop()
                temp = ''.join(temp)
                print temp
                to_file.write(str(temp)+'\n')
                contact_list.append(temp)
                
        check()
      
        cross = driver.find_element_by_class_name('_1aTxu').click()
        time.sleep(3)
        back = driver.find_element_by_class_name('C28xL')
        back.click()
        time.sleep(3)


        concatenate(contact_list)
        #print contact_list
    except :
        pass

to_file.close()
from_file.close()
driver.close()
sys.exit()
