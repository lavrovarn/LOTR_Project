import numpy as np
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


def download_characters_from_web(page_urls):
    
    """
    This function takes a list of URLs for pages containing character information for books and scrapes the data to create three lists: one with information about the characters, one with information about the books, and one that links the two together. The function uses Selenium WebDriver to automate the process of clicking through pages and extracting data from them. The output is returned as a pandas DataFrame containing information on all the characters found across the input pages.

    Parameters:
    - page_urls: A list of URLs for web pages containing character information for books.

    Returns:
    - A pandas DataFrame containing information about all the characters found on the input pages, along with information on the books they appear in.
    """
    
    
    # Create driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Initialize lists to store character and book data
    characters_list = [] # List with book's key and name 
    books_list=[] # List of dictionaries with book data
    book_character_list=[] # List of dictionaries with book-character relationship data
    
    # Initialize book and character indices
    book_index=0
    character_index=0
    
    
    for page_url in page_urls: 
        # Load the web page
        driver.get(page_url)

        # Handle cookie pop-up if present
        cookie_buttons = driver.find_elements(By.XPATH, '//div[text()="ANNEHMEN"]')
        if len(cookie_buttons) > 0:
            cookie_buttons[0].click()
        
        # Extract the name of the book from the web page
        book_name=driver.find_element(By.CLASS_NAME, 'page-header__title').text

        # Find the table of characters on the web page
        table_with_characters=driver.find_element(By.CLASS_NAME, 'appearances')
        character_elements=table_with_characters.find_elements(By.TAG_NAME, 'li')

        # Save each character's data
        for character in character_elements:
            
            character_url=character.find_element(By.TAG_NAME, 'a').get_attribute('href')
            character_name=character.find_element(By.TAG_NAME, 'a').text

            # Check if there is additional info for this character
            additional_info=character.find_elements(By.TAG_NAME, 'small')
            if(len(additional_info)>0):
                # Extract the additional info and split it into separate fields
                character_add_infos=character.find_element(By.TAG_NAME, 'small').text
                character_add_info = character_add_infos.split(", ") # Split string if there are many other names
                character_add_info = character_add_infos.replace(") (", ", ").replace(")", "").replace("(", "")
            else:
                character_add_info=None

            # Check if this character has already been added to the characters list
            if (next((item for item in characters_list if item["character_name"] ==character_name), None))==None: 
                
                # Open the character's web page to extract additional information
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[1])
                driver.get(character_url)
                
                try:
                    # Extract other names for the character
                    other_names_section=driver.find_element(By.XPATH, '//div[@data-source="othernames"]')
                    other_names_str=other_names_section.find_element(By.CLASS_NAME, 'pi-data-value').text
                    other_names_str = re.sub('\[\d\]', '', other_names_str)
                    other_names_str=other_names_str.replace(",\n","; ")
                    other_names_str=other_names_str.replace("\n","; ")
                    other_names_str=other_names_str.replace(", ","; ")
                    other_names=other_names_str.split("; ")
                except NoSuchElementException:
                    other_names=[]
                
                # Close the character's web page
                driver.close()
                
                # Switch to old tab
                driver.switch_to.window(driver.window_handles[0])        
         
                # Add the character to the characters list and the book-character list
                characters_list.append({
                    "character_key": character_index,
                    "character_name": character_name,
                    "character_firstname": character_name.split(' ', 1)[0],
                    "other_names": other_names,
                    "character_url": character_url
                })
                book_character_list.append({
                    "book_key": book_index, 
                    "character_key": character_index,
                    "add_info": character_add_info
                })
                character_index=character_index+1
            else: 
                book_character_list.append({
                    "book_key": book_index, 
                    "character_key": next(item for item in characters_list if item["character_name"] ==character_name)["character_key"], 
                    "add_info": character_add_info
                })

                
        books_list.append({"key": book_index, "name": book_name})
        book_index=book_index+1
       
    # Close the driver
    driver.close()
    
    # Create a pandas DataFrame from the characters_list
    characters_list_df=pd.DataFrame(characters_list)
    
    # Return the characters_list DataFrame
    return characters_list_df



def compare_two_sources(characters_list_df, page_url):
   
    """
    Compares two sources of character data and updates a dataframe of characters with new entries.

    Parameters:
    characters_list_df (pd.DataFrame): a dataframe containing existing character data
    page_url (str): the URL of the webpage containing the new character data

    Returns:
    pd.DataFrame: a dataframe containing all the characters from both sources
    """
    #get all characters from book
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(page_url)

    #list with characters from second source 
    book_characters=[]

    book_characters_unique=[]

    #find div with characters 
    book_table_with_characters=driver.find_element(By.CLASS_NAME, 'mw-category')

    #find all characters inside of div with characters 
    book_character_elements=book_table_with_characters.find_elements(By.TAG_NAME, 'a')

    [book_characters.append({"character_name": character.text, "character_url": character.get_attribute('href')}) for character in book_character_elements]

    last_index_of_df=characters_list_df['character_key'].tail(1).index[0]
    for i, item in enumerate(book_characters):
        if item["character_name"] not in list(characters_list_df.character_name) and item["character_name"].split(' ', 1)[0] not in list(characters_list_df.character_firstname):
            print(item["character_name"])
            last_index_of_df=last_index_of_df+1
            characters_list_df.loc[len(characters_list_df.index)] = [last_index_of_df, item["character_name"], item["character_name"].split(' ', 1)[0], [], item["character_url"]]
            book_characters_unique.append(item)
    driver.close()    
    return characters_list_df

    
def get_book_text(book_name):
    
    """
    Returns a Spacy Doc object containing NER (Named Entity Recognition) annotations for the given book text file.

    Args:
    - book_name (str): The name of the book text file to read.

    Returns:
    - Spacy Doc: A Spacy Doc object containing NER annotations for the book text.
    """

    # Load spacy English languague model
    NER=spacy.load("en_core_web_sm")
    # Read book text from file
    with open(book_name, 'r', encoding='utf-8') as file:
        book_text = file.read()
        
        # Process book text with spacy NER model
        book_doc = NER(book_text)
        
    return book_doc

def get_entity_list_per_sentence(book_doc):
    
    """
    Extract named entities per sentence from spacy parsed document of a book.
    
    Args:
    - book_doc (spacy.tokens.Doc): Parsed spacy document of the book text.
    
    Returns:
    - sent_entity_df (pandas.DataFrame): Dataframe with named entities per sentence.
    """
    
    sent_entity_df=[]
    
    # Loop through sentences, store named entity list for each sentence
    for sent in book_doc.sents: 
        entity_list=[ent.text for ent in sent.ents]
        sent_entity_df.append({"sentence": sent, "entities": entity_list})
    
    # Convert list of dictionaries to pandas dataframe
    sent_entity_df=pd.DataFrame(sent_entity_df) 
    return sent_entity_df

def filter_entity(ent_list, character_df): 
    
    """
    This function takes in a list of named entities and a dataframe of characters, and returns a filtered list of named entities
    where each entity is a character from the input dataframe or one of their alternative names.

    Args:
    - ent_list: a list of strings representing named entities
    - character_df: a pandas dataframe containing a list of characters and their alternative names

    Returns:
    - ent_list_final: a list of strings representing named entities that match a character from the input dataframe or one of their alternative names
    """
    
    ent_list_final=[]
    
    # Loop through each named entity in the list
    for ent in ent_list:
        
        # Check if entity matches a character name in the dataframe
        if ent in list(character_df.character_name):
            index=list(character_df.character_name).index(ent)
            ent_list_final.append(character_df.character_name[index])
        
        # Check if entity matches a character first name in the dataframe
        elif ent in list(character_df.character_firstname):
            index=list(character_df.character_firstname).index(ent)
            ent_list_final.append(character_df.character_name[index])
            
        # Check if entity matches one of the alternative names for a character in the dataframe
        else: 
            for num, other_names in enumerate(list(character_df.other_names)):
                if ent in other_names: 
                    ent_list_final.append(character_df.character_name[num])
                    
    return ent_list_final

def create_relationships (df, window_size): 
    
    """
    Creates a DataFrame of relationships between characters in a text based on the proximity of their mentions.
    
    Args:
    - df: a pandas DataFrame with a 'character_entities' column that contains lists of characters mentioned in each sentence
    - window_size: an integer representing the number of sentences to consider for each window
    
    Returns:
    - relationship_df: a pandas DataFrame with 'source', 'target', and 'value' columns representing the relationships between characters
    
    """
    
    # Initialize an empty list to store relationships
    relationships = []

    # Loop through each index in the DataFrame
    for i in range(df.index[-1]):
            
        # Define the end of the window
        end_i = min(i + window_size, df.index[-1])
        # Get a list of characters mentioned in the current window
        char_list = sum((df.loc[i: end_i].character_entities), [])
        
        # Remove duplicated characters that are next to each other
        char_unique = [char_list[i] for i in range(len(char_list)) 
                       if (i==0) or char_list[i] != char_list[i-1]]
        
        # If there are at least two unique characters in the window, create relationships between them
        if len(char_unique) > 1:
            for idx, a in enumerate(char_unique[:-1]):
                b = char_unique[idx + 1]
                relationships.append({"source": a, "target": b})
    
    # Convert the list of relationships to a DataFrame     
    relationship_df = pd.DataFrame(relationships)
   
    # Sort the cases with a->b and b->a
    relationship_df = pd.DataFrame(np.sort(relationship_df.values, axis = 1), columns = relationship_df.columns)

    # Add a 'value' column to count the number of occurrences of each relationship
    relationship_df["value"] = 1
    # Group by 'source' and 'target' to aggregate the relationships
    relationship_df = relationship_df.groupby(["source","target"], 
                                              sort=False, 
                                              as_index=False).sum()
                
    return relationship_df           