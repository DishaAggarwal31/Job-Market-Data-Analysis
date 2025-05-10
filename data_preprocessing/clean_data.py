import pandas as pd
import re
import numpy as np
import json
from utils.helpers import save_to_csv

#print(talent_df.head(5))

def preprocessing_main():
    print('Fetching and cleaning the data files.....')
    file_path = 'data/raw/'

    talent_df = pd.read_csv(file_path+'jobs_talent_data.csv', index_col = 'job_id')
    monster_df = pd.read_csv(file_path+'jobs_monster_data.csv', index_col = 'job_id')
    naukri_df = pd.read_csv(file_path+'Naukridotcom_Job_postings.csv', usecols = ['Job Title', 'Company', 'Location', 'Experience'])
    linkedln_df = pd.read_csv(file_path+'linkedln_jobs_india.csv', index_col = 'id', usecols = ['id', 'title', 'companyName', 'experienceLevel', 'sector', 'city', 'state'])

    talent_df, monster_df, naukri_df, linkedln_df = clean_exp_years(talent_df, monster_df, naukri_df, linkedln_df)
    talent_df, monster_df, naukri_df, linkedln_df = derive_experience_category(talent_df, monster_df, naukri_df, linkedln_df)
    talent_df, monster_df, naukri_df, linkedln_df = derive_industry(talent_df, monster_df, naukri_df, linkedln_df)
    talent_df, monster_df, naukri_df, linkedln_df = derive_city_state(talent_df, monster_df, naukri_df, linkedln_df)
    talent_df, monster_df, naukri_df, linkedln_df = divide_rows_for_multiple_locations(talent_df, monster_df, naukri_df, linkedln_df)
    print('All columns and rows are derived..')
    talent_df, monster_df, naukri_df, linkedln_df = columns_standardization(talent_df, monster_df, naukri_df, linkedln_df)
    print('Standardization of multiple files completed ....')
    create_cleaned_data(talent_df, monster_df, naukri_df, linkedln_df)
    print('Preprocessed Files created.')


def clean_exp_years(talent_df, monster_df, naukri_df, linkedln_df):
    # Create or derive the experience range
    talent_df['experience_range'] = talent_df['job_title'].apply(extract_experience_years_range)
    monster_df['experience_range'] = monster_df.apply(lambda row: extract_experience_years_range(row['job_title'], row['experience']), axis=1)
    naukri_df['experience_range'] = naukri_df.apply(lambda row: extract_experience_years_range(row['Job Title'], row['Experience']), axis=1)
    linkedln_df['experience_range'] = linkedln_df.apply(lambda row: extract_experience_years_range(row['title'], row['experienceLevel']), axis=1)

    # Derive the experience (average of range)
    talent_df['Experience (In Years)'] = talent_df['experience_range'].apply(convert_exp_range_to_years)
    monster_df['Experience (In Years)'] = monster_df['experience_range'].apply(convert_exp_range_to_years)
    naukri_df['Experience (In Years)'] = naukri_df['experience_range'].apply(convert_exp_range_to_years)
    linkedln_df['Experience (In Years)'] = linkedln_df['experience_range'].apply(convert_exp_range_to_years)

    return talent_df, monster_df, naukri_df, linkedln_df

def derive_experience_category(talent_df, monster_df, naukri_df, linkedln_df):
    talent_df['Experience Category'] = talent_df['Experience (In Years)'].apply(categorize_experience)
    monster_df['Experience Category'] = monster_df['Experience (In Years)'].apply(categorize_experience)
    naukri_df['Experience Category'] = naukri_df['Experience (In Years)'].apply(categorize_experience)
    linkedln_df['Experience Category'] = linkedln_df['Experience (In Years)'].apply(categorize_experience)

    return talent_df, monster_df, naukri_df, linkedln_df

def derive_industry(talent_df, monster_df, naukri_df, linkedln_df):
    talent_df['Industry'] = talent_df['job_title'].apply(categorize_industry)
    monster_df['Industry'] = monster_df['job_title'].apply(categorize_industry)
    naukri_df['Industry'] = naukri_df['Job Title'].apply(categorize_industry)
    linkedln_df['Industry'] = linkedln_df.apply(lambda row: categorize_industry(row['title'], row['sector']), axis=1)
    return talent_df, monster_df, naukri_df, linkedln_df

def derive_city_state(talent_df, monster_df, naukri_df, linkedln_df):
    # 5. Apply city extraction
    talent_df[['City', 'State', 'Country']] = talent_df['location'].apply(lambda loc: pd.Series(extract_cities_and_states(loc)))
    naukri_df[['City', 'State', 'Country']] = naukri_df['Location'].apply(lambda loc: pd.Series(extract_cities_and_states(loc)))
    monster_df[['City', 'State', 'Country']] = monster_df['location'].apply(lambda loc: pd.Series(extract_cities_and_states(loc)))
    linkedln_df[['City', 'State', 'Country']] = linkedln_df['city'].apply(lambda loc: pd.Series(extract_cities_and_states(loc)))
    return talent_df, monster_df, naukri_df, linkedln_df

def divide_rows_for_multiple_locations(talent_df, monster_df, naukri_df, linkedln_df):
    # 6. Explode into multiple rows if multiple cities exist
    talent_df = talent_df.explode(['City', 'State', 'Country'])
    naukri_df = naukri_df.explode(['City', 'State', 'Country'])
    monster_df = monster_df.explode(['City', 'State', 'Country'])
    linkedln_df = linkedln_df.explode(['City', 'State', 'Country'])

    return talent_df, monster_df, naukri_df, linkedln_df

def columns_standardization(talent_df, monster_df, naukri_df, linkedln_df):
    linkedln_df['Company Name'] = linkedln_df['companyName']
    naukri_df['Company Name'] = naukri_df['Company']
    talent_df['Company Name'] = talent_df['company_name']
    monster_df['Company Name'] = monster_df['company_name']

    linkedln_df['Job Title'] = linkedln_df['title']
    naukri_df['Job Title'] = naukri_df['Job Title']
    talent_df['Job Title'] = talent_df['job_title']
    monster_df['Job Title'] = monster_df['job_title']

    linkedln_df['Source'] = 'LinkedLn'
    naukri_df['Source'] = 'Naukri'
    talent_df['Source'] = talent_df['source']
    monster_df['Source'] = monster_df['source']

    return talent_df, monster_df, naukri_df, linkedln_df

def create_cleaned_data(talent_df, monster_df, naukri_df, linkedln_df):
    selected_columns = ['Job Title', 'Company Name', 'Experience (In Years)', 'Experience Category', 'Industry', 'City', 'State', 'Country', 'Source']
    cleaned_linkedln_df = linkedln_df[selected_columns].copy()
    cleaned_monster_df = monster_df[selected_columns].copy()
    cleaned_talent_df = talent_df[selected_columns].copy()
    cleaned_naukri_df = naukri_df[selected_columns].copy()

    # create CSV files
    folder = 'data/cleaned/'
    save_to_csv(cleaned_linkedln_df, 'cleaned_linkedln_df.csv', folder)
    save_to_csv(cleaned_monster_df, 'cleaned_monster_df.csv', folder)
    save_to_csv(cleaned_talent_df, 'cleaned_talent_df.csv', folder)
    save_to_csv(cleaned_naukri_df, 'cleaned_naukri_df.csv', folder)

# This method calculate years of experience needed based on job title if exp is not given
def extract_experience_years_range(title, exp = ''):
    title = title.lower()
    exp = exp.lower()

    # Check if exp values are valid
    if any(term in exp for term in ['years', 'yrs', 'yr']):
        return exp
    
    # Approximate based on seniority terms
    if any(term in exp for term in ['president', 'ceo', 'cto', 'executive']) or any(term in title for term in ['president', 'ceo', 'cto', 'executive']):
        return '18-25 Years'
    elif any(term in exp for term in ['vice president', 'vp', 'vice']) or any(term in title for term in ['vice president', 'vp', 'vice']):
        return '15-20 Years'
    elif any(term in exp for term in ['director', 'head', 'chief']) or any(term in title for term in ['director', 'head', 'chief']):
        return '11-15 Years'
    elif any(term in exp for term in ['manager']) or any(term in title for term in ['manager']):
        return '6-10 Years'
    elif any(term in exp for term in ['specialist', 'administrator', 'scientist']) or any(term in title for term in ['scientist', 'specialist', 'administrator']):
        return '5-8 Years'
    elif any(term in exp for term in ['architect']) or any(term in title for term in ['architect']):
        return '5-10 Years'
    elif any(term in exp for term in ['senior', 'lead', 'sr', 'sr.']) or any(term in title for term in ['senior', 'lead', 'sr', 'sr.']):
        return '4-7 Years'
    elif any(term in exp for term in ['analyst']) or any(term in title for term in ['analyst']):
        return '2-5 Years'
    elif any(term in exp for term in ['mid', 'associate']) or any(term in title for term in ['mid', 'associate']):
        return '2-3 Years'
    elif any(term in exp for term in ['jr', 'jr.', 'junior', 'entry', 'graduate', 'intern', 'fresher', 'internship']) or any(term in title for term in ['jr', 'jr.','internship', 'junior', 'entry', 'graduate', 'intern', 'fresher']):
        return '0 Years'

    return '1-5 Years' # Unknown

# I need to calculate the experience in years based on experince range for all datasets
def convert_exp_range_to_years(exp_str):
    if pd.isnull(exp_str):
        return np.nan

    exp_str = exp_str.lower().strip()

    # Match ranges like '2-4 years', '1 - 3 yrs'
    range_match = re.findall(r'(\d+)\s*[-–]\s*(\d+)', exp_str)
    if range_match:
        low, high = map(int, range_match[0])
        return round((low + high) / 2, 1)

    # Match single year like '0 years' or '5 yrs'
    single_match = re.search(r'(\d+)', exp_str)
    if single_match:
        return float(single_match.group(1))

    return np.nan

def categorize_experience(years):
    if years < 1:
        return 'Entry'
    elif years <= 3:
        return 'Junior'
    elif years <= 6:
        return 'Mid-Level'
    elif years <= 8:
        return 'Senior'
    elif years <= 12:
        return 'Lead'
    elif years <= 15:
        return 'Manager'
    else:
        return 'Executive'

#  a method to determine the industry of the job as it will be helpful during data analytics!!
def categorize_industry(job_title, sector = ''):
    title = job_title.lower()
    sector = str(sector).lower()
    
    if any(keyword in sector for keyword in ['mechanical', 'industrial', 'consumer', 'motor', 'manufacturing', 'retail', 'furniture', 'wholesale', 'building', 'food', 'education', 'sports', 'telecommunications', 'construction', 'civil', 'coaching', 'teach', 'fashion']):
        return 'Other'
    
    if any(keyword in title for keyword in ['gen ai', 'generative ai', 'llm', 'artificial intelligence', 'ai ', 'machine learning', 'ml ']):
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
    elif any(keyword in title for keyword in ['accountant', 'finance', 'auditor', 'chartered', 'retail']):
        return 'Finance'
    elif any(keyword in title for keyword in ['marketing', 'seo', 'digital']):
        return 'Marketing'
    elif any(keyword in title for keyword in ['sales', 'business development', 'business analyst', 'business']):
        return 'Buisness Analytics'
    elif any(keyword in title for keyword in ['consulting', 'consultant']):
        return 'Consulting'
    elif 'manager' in title or 'management' in title or title.endswith(' manager'):
        return 'Management'
    elif any(keyword in title for keyword in ['hr', 'recruiter', 'talent', 'recruiting', 'recruit']):
        return 'Human Resources'
    elif any(keyword in title for keyword in ['technical', 'it ', 'technical support']):
        return 'Information Technology'
    else:
        return 'Other'


# 3. Define a function to extract all cities from a raw location string
def extract_cities_and_states(location_str):

    # 1. Load your hierarchical city-state JSON
    folder = 'data/json files/'
    filepath = folder + 'city_state_map.json'
    with open(filepath, 'r', encoding='utf-8') as f:
        city_state_map = json.load(f)

    # 2. Flatten city list with state
    city_to_state = {
        city.lower(): state for state, cities in city_state_map.items() for city in cities
    }

    REMOTE_TERMS = {'remote', 'work from home', 'wfh', 'pan india'}

    # Common corrections for alternate/misspelled city names
    city_normalization_map = {
        'gurugram': 'gurgaon',
        'bengaluru': 'bangalore',
        'bangalore': 'bengaluru',
        'new delhi': 'delhi',
        'delhi': 'new delhi',
        'ncr': 'delhi',
        'gurgaon': 'gurgaon',
        'banglore': 'bengaluru'
            }
        
    if not isinstance(location_str, str):
        return [np.nan], [np.nan], [np.nan]

    parts = re.split(r'[\/,|-]', location_str.lower())
    matched_cities = []
    matched_states = []
    country = []

    for part in parts:
        part_cleaned = part.strip()
        # Clean the part in case any additional ()
        part_cleaned = re.sub(r'\(.*?\)', '', part_cleaned).strip()
        
        # Hndling remote location cases
        if part_cleaned in REMOTE_TERMS:
            matched_cities.append('Remote')
            matched_states.append('Remote')
            country.append('Remote')
            
        # Normalize known variants
        if part_cleaned not in city_to_state:
            part_cleaned = city_normalization_map.get(part_cleaned, part_cleaned)
                
        if part_cleaned in city_to_state:
            matched_cities.append(part_cleaned.title())
            matched_states.append(city_to_state[part_cleaned])
            country.append('India')
        # Check if state exists in location:
        elif part_cleaned in city_state_map:
            matched_cities.append(np.nan)
            matched_states.append(part_cleaned.title())
            country.append('India')
        else:
            for city in city_to_state:
                if city in part_cleaned:
                    matched_cities.append(city)
                    matched_states.append(city_to_state[city])
                    country.append('India')
            
    if len(matched_cities) == 0:
        if 'india' in location_str.lower():
            return [np.nan],[np.nan], ['India']
        return [np.nan], [np.nan], [np.nan]
    return matched_cities, matched_states, country

