from utils.helpers import *

# This method takes in the webpage and extract data and store in a dictionary datastructure jobs
def fetch_jobs_from_talent(talent_doc):
    talent_jobs_class = 'sc-8e83a395-1 eIzOpw'
    talent_jobs_data = talent_doc.find_all('section', class_ = talent_jobs_class)

    job_title_class = 'sc-6f9356d1-20 sc-6f9356d1-23 hOTlXX giCKXi'
    company_class = 'sc-6f9356d1-10 sc-6f9356d1-12 jHSVbo gyxIYw'
    location_class = 'sc-6f9356d1-10 sc-6f9356d1-11 aSgez bNXZmD'
    job_url_class = 'sc-6f9356d1-5 sc-6f9356d1-8 sc-d93925ca-5 eDTPEZ gjefvX kEITSw'
    image_class = 'sc-5c54c4fb-1 ixNEQE'

    jobs = {
            'job_id' : [],
            'job_title' : [],
            'company_name' : [],
            'location' : [],
            #'industry' : [],
            #'job_position': [],
            #'experience' : [],
            'source' : []
    }
    
    for job_data in talent_jobs_data:
        try:
            job_title = job_data.find('h2', job_title_class).text
            company = job_data.find('span', company_class).text
            location = job_data.find('span', location_class).text
            job_url = 'https://in.talent.com/' + job_data.find('a', job_url_class)['href']
            #image = talent_jobs_data[0].find('div', 'sc-5c54c4fb-1 ixNEQE').find('img')['src'] # Can use further as required to display in frontend

            #fetch_talent_details_from_job_specific_url(job_url)
            jobs['job_id'].append(generate_job_id('talent'))
            jobs['job_title'].append(job_title)
            jobs['company_name'].append(company)
            jobs['location'].append(location)
            jobs['source'].append('Talent')
            #jobs['application_link'].append(job_url)
            #jobs['industry'].append(categorize_industry(job_title))
            #jobs['job_position'].append(get_job_position_level(job_title))
            #jobs['experience'] = extract_years_from_title(job_title)
        except Exception as e:
            print(f"Error processing a job card: {e}")
            continue
    return jobs

def talent_main(keyword, location, company, exp):
    # User input for search keyword and location
    # keyword, location, company, exp = input_from_users()
    # the website URL customised to add serach filters and Format the serach URL as per standard url format
    #https://in.talent.com/jobs?k=manager&l=Delhi%2C+IN&empname=accenture
    
    talent_search_url = 'https://in.talent.com/jobs?k={}&l={}'
    talent_formatted_url = ''
    if len(company.strip()) > 0:
        talent_search_url = 'https://in.talent.com/jobs?k={}&l={}%2C+IN&empname={}'
        talent_formatted_url = talent_search_url.format(format_str(keyword, 'talent'), format_str(location, 'talent'), format_str(company, 'talent'))
    else:
        talent_formatted_url = talent_search_url.format(format_str(keyword, 'talent'), format_str(location, 'talent'))
    # Open and access the webpage
    print('Accessing the webpage {}...'.format(talent_formatted_url))
    talent_doc = get_webpage(talent_formatted_url)
    print('Please Wait! Fetching the jobs...')
    # Fetch the list of jobs
    jobs = fetch_jobs_from_talent(talent_doc)
    print('Completed!')
    # Create a dataframe for jobs
    df_jobs = pd.DataFrame(jobs)
    print(df_jobs)
    # Create / Append the CSV file the jobs data
    print('Saving the data to CSV file...')
    filename = 'jobs_talent_data.csv'
    save_to_csv(df_jobs, filename, 'data/raw')
    print('File named {} created/ updated.'.format(filename))
    return



