
import urllib.parse
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .global_variables import job_id_counter, save_job_id_counter

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

# This method generate the unique ID as per source
def generate_job_id(source):
    source_key = source.lower()
    job_id_counter[source_key] += 1

    prefix = {
        'talent': 'TAL',
        'monster': 'MON'
    }.get(source_key, 'GEN')

    # Save the updated counter to file
    save_job_id_counter(job_id_counter)

    return f"{prefix}{str(job_id_counter[source_key]).zfill(4)}"

# This method calculate years of experience needed based on job title if exp is not given
def extract_years_from_title(title):
    title = title.lower()
    
    # Common patterns
    import re
    match = re.search(r'(\d+)\+?\s*(?:years|yrs)', title)
    if match:
        return int(match.group(1))
    
    # Approximate based on seniority terms
    if any(term in title for term in ['director', 'head', 'vp', 'chief']):
        return '10+ years'
    elif 'manager' in title:
        return '6-10 Years'
    elif any(term in title for term in ['senior', 'lead']):
        return '4-6 Years'
    elif any(term in title for term in ['mid', 'associate']):
        return '2-3 years'
    elif any(term in title for term in ['junior', 'entry', 'graduate', 'intern']):
        return '0 Years'

    return '1-5 Years' # Unknown

#  a method to determine the industry of the job as it will be helpful during data analytics!!
def categorize_industry(job_title):
    title = job_title.lower()

    if any(keyword in title for keyword in ['gen ai', 'generative ai', 'llm', 'artificial intelligence', 'ai', 'machine learning', 'ml']):
        return 'Artificial Intelligence / Machine Learning'
    elif any(keyword in title for keyword in ['cloud', 'aws', 'azure', 'gcp']):
        return 'Cloud'
    elif any(keyword in title for keyword in ['data scientist', 'data analyst', 'analytics', 'data', 'etl']):
        return 'Data Science / Analytics'
    elif any(keyword in title for keyword in ['web developer', 'web development', 'front end', 'frontend', 'html', 'css', 'javascript', 'react', 'web designer']):
        return 'Web Development'
    elif 'devops' in title:
        return 'DevOps'
    elif 'qa' in title or 'quality assurance' in title or 'test' in title or 'tester' in title:
        return 'Quality Assurance / Testing'
    elif any(keyword in title for keyword in ['software', 'developer', 'engineer', 'backend', 'frontend', 'full stack', 'architect', 'designer']):
        return 'Software Development'
    elif any(keyword in title for keyword in ['accountant', 'finance', 'auditor', 'chartered']):
        return 'Finance'
    elif any(keyword in title for keyword in ['marketing', 'seo', 'digital']):
        return 'Marketing'
    elif any(keyword in title for keyword in ['sales', 'business development', 'business analyst', 'business']):
        return 'Buisness Analytics'
    elif any(keyword in title for keyword in ['consulting', 'consultant']):
        return 'Consulting'
    elif 'manager' in title or 'management' in title or title.endswith(' manager'):
        return 'Management'
    elif any(keyword in title for keyword in ['hr', 'recruiter', 'talent']):
        return 'Human Resources'
    else:
        return 'Other'

# a method to determine the position level of the job as it will be helpful during data analytics!!
def get_job_position_level(title):
    title = title.lower()
    
    if "intern" in title or "trainee" in title:
        return "Intern"
    elif "manager" in title:
        return "Manager"
    elif "junior" in title or "jr." in title or "fresher" in title or "graduate" in title or ' i ' in title or '-i' in title:
        return "Entry"
    elif "senior" in title or "sr." in title or "sr" in title or ' ii ' in title or ' iii ' in title:
        return "Senior"
    elif "lead" in title or '-ii' in title or '-iii' in title:
        return "Senior"
    elif "director" in title or "head" in title:
        return "Director"
    elif any(x in title for x in ["vp", "vice president", "chief", "ceo", "cto", "coo", "cfo"]):
        return "Executive"
    else:
        return "Mid"

# Let's save the results in the csv file for each execution and build sample data for analysis and visulation
def save_jobs_to_csv(df, filename='jobs_data.csv'):
    folder = 'data'
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
    
    driver.save_screenshot("debug_page.png")
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'srpResultCardContainer'))
        )
    except Exception as e:
        print("Error waiting for element. Cannot find the element.")
        
    doc = BeautifulSoup(driver.page_source, 'html.parser')
    
    driver.quit()
    return doc


