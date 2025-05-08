
import urllib.parse
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from .global_variables import job_id_counter, save_job_id_counter

# This method takes in the parameters and format it as per webiste's formatting - 
# Convert spaces to + or - (depending on the site).
# Convert text to lowercase if required.
# Remove special characters if needed.
def format_str(word, site):
    formatted_word = word.strip()
    if site == 'indeed' or site == 'talent' or site == 'monster':
        formatted_word = urllib.parse.quote(formatted_word)
        formatted_word = formatted_word.replace('%20','+')
    elif site == 'linkedln':
        formatted_word = urllib.parse.quote(formatted_word)
        
    return formatted_word

# a function to extract the page which takes the URL as input and returns a beautifulsoap object containing the page HTML object.
def get_webpage(page_url):
    # Get the page from the given URL
    response = requests.get(page_url)
    # Check the status of the page is successful else print the error
    if response.status_code != 200:
        raise Exception('Failed to load page {}'.format(page_url))
    # Parse the web page to beautiful soup
    doc = BeautifulSoup(response.text, 'html.parser')
    return doc


def load_job_id_counter(COUNTER_FILE, folder):
    filepath = os.path.join(folder, COUNTER_FILE)

    # Check if file already exists
    file_exists = os.path.isfile(filepath)
    
    if file_exists:
        with open(filepath, "r") as file:
            return json.load(file)
    else:
        return {'talent': 0, 'monster': 0}


# This method generate the unique ID as per source
def generate_job_id(source):
    COUNTER_FILE = "job_id_counter.json"
    folder = 'data/json files'
    job_id_counter = load_job_id_counter(COUNTER_FILE, folder)
    
    source_key = source.lower()
    job_id_counter[source_key] += 1

    prefix = {
        'talent': 'TAL',
        'monster': 'MON'
    }.get(source_key, 'GEN')

    # Save the updated counter to file
    save_to_json(job_id_counter, COUNTER_FILE, folder)

    return f"{prefix}{str(job_id_counter[source_key]).zfill(4)}"


# Let's save the results in the csv file for each execution and build sample data for analysis and visulation
def save_to_csv(df, filename, folder):
    #folder = 'data/raw'
# Ensure the folder exists
    os.makedirs(folder, exist_ok=True)

    # Full path to the file
    filepath = os.path.join(folder, filename)

    # Check if file already exists
    file_exists = os.path.isfile(filepath)

    # Save the DataFrame
    df.to_csv(
        filepath,
        mode='a' if file_exists else 'w',
        index=False,
        header=not file_exists,
        encoding='utf-8'
    )
    print(f"Saved to {filepath}")

def save_to_json(df, filename, folder):
    os.makedirs(folder, exist_ok=True)

    # Full path to the file
    filepath = os.path.join(folder, filename)

    # Check if file already exists
    file_exists = os.path.isfile(filepath)
    
    # Save to a JSON file
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(df, f, ensure_ascii=False, indent=4)
    
    print(f"Saved to {filepath}")

# Function for input
def input_from_users():
    keyword = input('Enter skill, position or title: ')
    location = input('Enter the location: ')
    company = input('Search by company: ')
    experience = input('Search by experience (in years):')

    keyword = keyword if keyword else 'Developer'# Its a mandatory field
    location = location if location else 'India'
    #experience = str(int(float(experience))) if float(experience) <= 40 else ''   # Take the values upto 40 only else invalid
    
    return keyword, location, company, experience

# A method to load a webpage using Selenium
def get_webpage_selenium(url):
    driver = webdriver.Chrome()

    driver.get(url)
    
    #driver.save_screenshot("debug_page.png")
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'srpResultCardContainer'))
        )
    except Exception as e:
        print("Error waiting for element. Cannot find the element.")
        
    doc = BeautifulSoup(driver.page_source, 'html.parser')
    
    driver.quit()
    return doc


