import pandas as pd
import time
import matplotlib.pyplot as plt
import re
import spacy
import os
import networkx as nx 

from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException





def download_characters_from_web(page_url):
    # Create driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    actions = ActionChains(driver)
     
    # list with character's key, name and url to his website
    characters_list = [] 
    # list with book's key and name 
    books_list=[] 
    # pivot-Table with book key and character key
    book_character_list=[] 
    #book key 
    book_index=0
    # character kex for all books
    character_index=0

    driver.get(page_url)

    #find div with characters 
    table_with_characters=driver.find_element(By.CLASS_NAME, 'mw-category')

    #find all characters inside of div with characters 
    character_elements=table_with_characters.find_elements(By.TAG_NAME, 'a')

    #save character
    for character in character_elements:
        character_url=character.get_attribute('href')
        character_name=character.text
        if "(" in character_name or ")" in character_name: 
            character_name=re.sub("[\(\[].*?[\)\]]", "", character_name)

        #get other names 

        # Open a new window
        driver.execute_script("window.open('');")

        # Switch to the new window and open new URL
        driver.switch_to.window(driver.window_handles[1])
        driver.get(character_url)

        try:
            other_names_section_header=driver.find_element(By.XPATH, "//td[contains(text(),'names')]")
            other_names_section_parent=other_names_section_header.find_element(By.XPATH, "..")
            other_names_section=other_names_section_parent.find_element(By.XPATH, ".//td[contains(text(),'names')=false]")
            other_names=other_names_section.text.split("\n")
            other_names=[other_name for other_name in other_names if 'below' not in other_name]
            other_names= [re.sub("[\(\[].*?[\)\]]", "", other_name) for other_name in other_names]
            other_names= [other_name.replace('\"','') for other_name in other_names]
        except NoSuchElementException:
            other_names=[]
        # Closing new_url tab
        driver.close()

        # Switching to old tab
        driver.switch_to.window(driver.window_handles[0])        

        characters_list.append({"character_key": character_index, "character_name": character_name, "character_firstname":character_name.split(' ', 1)[0], "other_names": other_names, "character_url": character_url})
        character_index=character_index+1

    driver.close()
    characters_list_df=pd.DataFrame(characters_list)
    return characters_list_df




def download_characters_from_web_old(page_urls):
    # Create driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    actions = ActionChains(driver)

    # list with character's key, name and url to his website
    characters_list = [] 
    # list with book's key and name 
    books_list=[] 
    # pivot-Table with book key and character key
    book_character_list=[] 
    #book key 
    book_index=0
    # character kex for all books
    character_index=0
    
    
    for page_url in page_urls: 
        #open url 
        driver.get(page_url)

        #click accept cookies if popup shows
        #identify element
        coockies=driver.find_elements(By.XPATH, '//div[text()="ANNEHMEN"]')
        if(len(coockies)>0):
            driver.find_element(By.XPATH, '//div[text()="ANNEHMEN"]').click()  
        #save book name
        book_name=driver.find_element(By.CLASS_NAME, 'page-header__title').text

        #find div with characters 
        table_with_characters=driver.find_element(By.CLASS_NAME, 'appearances')
        #find all characters inside of div with characters 
        character_elements=table_with_characters.find_elements(By.TAG_NAME, 'li')

        #save character
        for character in character_elements:

            character_url=character.find_element(By.TAG_NAME, 'a').get_attribute('href')
            character_name=character.find_element(By.TAG_NAME, 'a').text

            #check if addiitional info exists
            additional_info=character.find_elements(By.TAG_NAME, 'small')
            if(len(additional_info)>0):
                character_add_infos=character.find_element(By.TAG_NAME, 'small').text
                character_add_info = character_add_infos.split(", ")
                character_add_info = character_add_infos.replace(") (", ", ").replace(")", "").replace("(", "")
            else:
                character_add_info=None
                 # Load a page 

            #get other names 

            # Open a new window
            driver.execute_script("window.open('');")

            # Switch to the new window and open new URL
            driver.switch_to.window(driver.window_handles[1])
            driver.get(character_url)
            try:
                other_names_section=driver.find_element(By.XPATH, '//div[@data-source="othernames"]')
                other_names_str=other_names_section.find_element(By.CLASS_NAME, 'pi-data-value').text
                other_names_str = re.sub('\[\d\]', '', other_names_str)
                other_names_str=other_names_str.replace(",\n","; ")
                other_names_str=other_names_str.replace("\n","; ")
                other_names_str=other_names_str.replace(", ","; ")
                other_names=other_names_str.split("; ")
            except NoSuchElementException:
                other_names=[]
            # Closing new_url tab
            driver.close()

            # Switching to old tab
            driver.switch_to.window(driver.window_handles[0])        

            #add character to characters_list and to book_character_list 
            if (next((item for item in characters_list if item["character_name"] ==character_name), None))==None: 
                characters_list.append({"character_key": character_index, "character_name": character_name, "character_firstname":character_name.split(' ', 1)[0], "other_names": other_names, "character_url": character_url})
                book_character_list.append({"book_key": book_index, "character_key": character_index, "add_info": character_add_info})
                character_index=character_index+1
            else: 
                book_character_list.append({"book_key": book_index, "character_key": next(item for item in characters_list if item["character_name"] ==character_name)["character_key"], "add_info": character_add_info})

        books_list.append({"key": book_index, "name": book_name})
        book_index=book_index+1
    driver.close()

    characters_list_df=pd.DataFrame(characters_list)
    return characters_list

    
def get_book_text(book_name):

    # Load spacy English languague model
    NER=spacy.load("book_name")
    book_text = open(file_name).read()
    book_doc = NER(book_text)
    
    return book_doc

