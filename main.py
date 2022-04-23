import os
import tempfile
os.environ["MPLCONFIGDIR"] = tempfile.gettempdir()


from googleapiclient.discovery import build
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


api_key = 'AIzaSyA3K8uy13NeCWneH43eW3GziIG7Y9suqAo'
channel_ids = ['UCk6hRWc7Y4p9UENKs2rFMpg'#ybp
               'UCCkXU_pKTN98ktKl0TnHjBg'#ansh,
               'UCCWi3hpnq_Pe03nGxuS7isg'#campusx
              ]

Youtube = build('youtube', 'v3', developerKey = api_key)

# function to get channel stats

def get_channel_stats(Youtube, channel_ids):
    all_data = []
  
    request = Youtube.channels().list(
    part="snippet,contentDetails,statistics",
    id=','.join(channel_ids))

    response = request.execute()

    for i in range(len(response['items'])):
      
      data = dict(channel_name = response['items'][i]['snippet']['title'],
                  subscribers = response['items'][i]['statistics']['subscriberCount'],
                  views = response['items'][i]['statistics']['viewCount'],
                  total_video = response['items'][i]['statistics']['videoCount'])
      all_data.append(data)
    return response

print(get_channel_stats(Youtube, channel_ids))