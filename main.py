from scrapers.monster_scraper import monster_main
from scrapers.talent_scraper import talent_main
from scrapers.utils.helpers import input_from_users

for i in range(0, 5):
    keyword, location, company, exp = input_from_users()
    print('Fetching Data from Monster/ FoundIt website ....')
    monster_main(keyword, location, company, exp)
    print('Fetching Data from Talent website ....')
    talent_main(keyword, location, company, exp)
    print('Thank you :)')

