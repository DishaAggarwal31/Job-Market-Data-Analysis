from utils.helpers import *
#from PROJECT_JOBS.utils.helpers import *


def monster_main(keyword, location, company, exp):
    # User input for search keyword and location
    # keyword, location, company, exp = input_from_users()
    # the website URL customised to add serach filters and Format the serach URL as per standard url format
    # https://www.foundit.in/srp/results?query=accenture&locations=india&experienceRanges=0~0&experience=0
    # https://www.foundit.in/srp/results?query=accenture&locations=india&experienceRanges=3~3&experience=3
    # https://www.foundit.in/srp/results?query=accenture&locations=india
    location = location if location else 'Delhi'
    monster_search_url = 'https://www.foundit.in/srp/results?query={}&locations={}'
    monster_formatted_url = ''
    if len(exp.strip()) > 0:
        monster_search_url = 'https://www.foundit.in/srp/results?query={}&locations={}&experienceRanges={}~{}&experience={}'
        monster_formatted_url = monster_search_url.format(format_str(keyword, 'monster'), format_str(location, 'monster'),
                                                             exp, exp, exp)
    else:
        monster_formatted_url = monster_search_url.format(format_str(keyword, 'monster'), format_str(location, 'monster'))
        
    # Open and access the webpage
    print('Accessing the webpage {}...'.format(monster_formatted_url))
    monster_doc = get_webpage_selenium(monster_formatted_url)
    print('Please Wait! Fetching the jobs...')
    # Fetch the list of jobs
    jobs = fetch_jobs_from_monster(monster_doc)
    print('Completed!')
    # Create a dataframe for jobs
    df_jobs = pd.DataFrame(jobs)
    print(df_jobs)
    # Create / Append the CSV file the jobs data
    print('Saving the data to CSV file...')
    filename = 'jobs_monster_data.csv'
    save_to_csv(df_jobs, filename, 'data/raw')
    print('File named {} created/ updated.'.format(filename))
    return

# A method to fetch jobs from monster
def fetch_jobs_from_monster(monster_doc):
    detailsclass = 'srpResultCardContainer'
    job_lists = monster_doc.find_all('div', class_ = detailsclass)

    jobs = {
            'job_id' : [],
            'job_title' : [],
            'company_name' : [],
            'location' : [],
            #'industry' : [],
            #'job_position': [],
            'experience' : [],
            'source' : []
    }

    for job in job_lists:
        try:
            job_title = job.find('div', class_ = 'jobTitle').text.strip()
            company = job.find('div', class_ = 'companyName').text.strip()
            location = job.find('div', class_ = 'details location').text.strip()
            exp = job.find('span', class_ = 'details').text.strip()

            jobs['job_id'].append(generate_job_id('monster'))
            jobs['job_title'].append(job_title)
            jobs['company_name'].append(company)
            jobs['location'].append(location)
            jobs['source'].append('Monster')
            #jobs['industry'].append(categorize_industry(job_title))
            jobs['experience'].append(exp)
            #jobs['job_position'].append(get_job_position_level(job_title))
        except Exception as e:
            print(f"Error processing a job data: {e}")
            continue
        
    return jobs
