from igscrapper import IGScrapper
import os
from dotenv import load_dotenv

load_dotenv()
scraper = IGScrapper(os.environ['USER'], os.environ['PASSWORD'])
followers = scraper.get_followers(scraper.profile_name)
following = scraper.get_following(scraper.profile_name)
scraper.quit()

result = []
for user in following:
    if user not in followers:
        result.append(user)
print(result)

# this code works!