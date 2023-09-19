from bs4 import BeautifulSoup
import os
import pickle as pkl
from tqdm.auto import tqdm
import pandas as pd

count=0
failed_count=0

# read all html files
html_files = os.listdir('html')

df_logs = pd.read_csv('logs.csv')
df_logs.columns=['id','url','title','episode_title']
id2url = {str(log.id): log.url for log in df_logs.itertuples()}


series_list=[]
episode_list=[]
synopsis_list=[]

# parse each file
for html_file in tqdm(html_files):
    # create soup
    soup = BeautifulSoup(open('html/%s' % html_file).read(), 'html.parser')
    
    index = html_file.replace('.html', '')
    

    # extract relevant data
    synopsis_elem = soup.find('drawer-more')

    if not synopsis_elem:
        url = id2url.get(index, '')
        # if 'rottentomatoes' in url:
        #     print(index, url)
        failed_count+=1
        continue

    # get synopsis and do something with it
    synopsis = synopsis_elem.get_text()
    # count+=1

    index=int(index)

    # print(type(index))
    # print(index)
    try:
        count+=1
        series_list.append(df_logs[df_logs['id']==index]['title'].to_list()[0])
        # print(df_logs[df_logs['id']==index]['title'].to_list()[0])

        episode_list.append(df_logs[df_logs['id']==index]['episode_title'].to_list()[0])
        # print(df_logs[df_logs['id']==index]['episode_title'].to_list()[0])

        synopsis_list.append(synopsis)
    except Exception as e:
        
        print(index)




print('Fail % =')

print(failed_count/len(html_files))

print(count)

dataset_dict={'series': series_list, 'episode': episode_list, 'rt_synopsis': synopsis_list}

df_dataset=pd.DataFrame.from_dict(dataset_dict)

df_dataset.to_csv('X_Crawl.csv')

    