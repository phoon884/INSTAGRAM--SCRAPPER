from igscrapper import IGScrapper
import os
from dotenv import load_dotenv

load_dotenv()
USER = ""
scraper = IGScrapper(os.environ['USER'], os.environ['PASSWORD'])
followers = scraper.get_followers(USER)
following = scraper.get_following(USER)
scraper.quit()

result = []
for user in following:
    if user not in followers:
        result.append(user)
print(result)