from googlesearch import search
import pandas as pd
import os
import requests
from tqdm.auto import tqdm
from fake_useragent import UserAgent
from time import sleep

# read csv
data = pd.read_excel('releaseTestDataset_20230701__GAL500.xlsx')
logs = []
ua = UserAgent()

try:
    # iterate over rows
    for index, row in enumerate(tqdm(data.itertuples(), total=len(data))):
        # output file
        html_file = os.path.join('html', '%s.html' % index)

        # check if already exists
        if os.path.exists(html_file):
            continue

        # build query
        query = 'site:rottentomatoes.com %s %s' % (row.seriesTitle, row.materialTitle)
        count = 0
        while count < 2:
        # search
            try:
                results = search(query, num=10, user_agent=ua.random)  #pause=random.randint(50,60)

                # get first result
                url = next(results)

                print(html_file, url)

                # download html
                r = requests.get(url)
                if 'Access Denied' in r.text:
                    print('Access Denied')
                    sleep(60 * 5)
                    raise Exception('Access Denied')


                with open(html_file, 'w') as f:
                    f.write(r.text)

                # log
                logs.append(dict(index=index, url=url, title=row.seriesTitle, episode_title=row.materialTitle))        
                break
            except Exception as e:
                print(e)
                if "Too Many Requests" in str(e):
                    print("429 Sleep")
                    sleep(45*60)
                print("Sleeping for 30 seconds")
                sleep(10)
                count += 1
finally:
    pd.DataFrame(logs).to_csv('logs.csv', index=False, mode='a', header=False)