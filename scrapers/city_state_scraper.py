from .utils.helpers import *
import pandas as pd
import numpy as np

def extract_data(doc):

    city_state_map = dict()
    
    tables = doc.find_all('table', style = 'text-align:right')
    for table in tables:
        #print(table)
        datarow = table.find_all('tr')
        for row in datarow[1:]:
            #print(row)
            taglist = row.find_all('a')
            city = taglist[0].text.strip()
            text = taglist[1].text.strip() 
            i = 1
            while text.startswith('['):
                i = i + 1
                text = taglist[i].text.strip()
            state = text if text else np.nan
            #print(city, ',', state)
            
            if state in city_state_map:
                city_state_map[state].append(city)
            else:
                city_state_map[state] = [city]
            
    return city_state_map
        
def evoke_scraper_main():
    wiki_url = 'https://en.wikipedia.org/wiki/List_of_cities_in_India_by_population'
    doc = get_webpage(wiki_url)
    json_file = extract_data(doc)

    print(json_file)
    # Create / Append the Json file the jobs data
    print('Saving the data to Json file...')
    filename = 'city_state_map.json'
    folder = 'data/json files'
    save_to_json(json_file, filename, folder)
    print('File named {} created/ updated.'.format(filename))
    return