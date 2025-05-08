from scrapers.monster_scraper import monster_main
from scrapers.talent_scraper import talent_main
from utils.helpers import input_from_users
import random

for i in range(0, 1):
    #keyword, location, company, exp = input_from_users()

    # Expanded sample input lists
    keywords = [
        'Data Engineer', 'ETL Developer', 'Big Data Engineer', 'Data Analyst', 'engineer', 'frontend', 'backend', 'AI', 'Cloud', 'Azure', 
        'Data Scientist', 'Machine Learning Engineer', 'Analytics Engineer', 'microservices', 'tester', 'automation', 'GCP', 'AWS'
        'Data Architect', 'SQL Developer', 'BI Developer', 'java', 'python', 'manager', 'specialist', 'pyspark', 'datastage'
    ]

    locations = [
        'Bangalore', 'Hyderabad', 'Pune', 'Chennai', 'Mumbai', 'Delhi', 'Gurgaon',
        'Noida', 'Kolkata', 'Ahmedabad', 'Remote', 'India', 'Meerut', ''
    ]

    companies = [
        'Amazon', 'TCS', 'Accenture', 'Infosys', 'Capgemini', 'Google', 'Microsoft',
        'Cognizant', 'HCL', 'Wipro', 'Flipkart', 'ZS Associates', 'Deloitte', 'EY', 'PwC', ''
    ]

    # Create experience values from 0 to 10 years
    experience_levels = str([i for i in range(0, 10)])

    # Example of choosing random values from each
    random_keyword = random.choice(keywords)
    random_location = random.choice(locations)
    random_company = random.choice(companies)
    random_exp = random.choice(experience_levels)

    print('Fetching Data from Monster/ FoundIt website ....')
    #monster_main(keyword, location, company, exp)
    monster_main(random_keyword, random_location, random_company, random_exp)
    print('Fetching Data from Talent website ....')
    #talent_main(keyword, location, company, exp)
    talent_main(random_keyword, random_location, random_company, random_exp)
    print('Iteration {} is completed'.format(i))

print('Thank you! :)')