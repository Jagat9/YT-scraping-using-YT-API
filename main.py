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

youtube = build('youtube', 'v3', developerKey = api_key)



def get_channel_stats(youtube, channel_ids):
  request = youtube.channels().list(part="snippet,contentDetails,statistics",
                                    id=','.join(channel_ids))

  response = request.execute()
  data = dict(channel_name = response["items "][0]['snippet']['title'])

  return response
  # return response

print(get_channel_stats(youtube, channel_ids))



























