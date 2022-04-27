import os
import tempfile
os.environ["MPLCONFIGDIR"] = tempfile.gettempdir()


from googleapiclient.discovery import build
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


api_key = 'AIzaSyA3K8uy13NeCWneH43eW3GziIG7Y9suqAo'
channel_ids = ['UCk6hRWc7Y4p9UENKs2rFMpg',#ybp
              'UCBGcs9XTL5U34oaSn_AsHqw',#elearing
              'UCyHta2dyCTkf29AB67AYn7A'#5minuteengineering
              ]

youtube = build('youtube', 'v3', developerKey = api_key)


# define a function to do the scraping statistics from api
def get_channel_stats(youtube, channel_ids):
  all_data = []
  request = youtube.channels().list(
    part = 'snippet,contentDetails,statistics',
    id = ','.join(channel_ids))
  response = request.execute()
  for i in range(len(response['items'])):
    data = dict(Channel_name = response['items'][i]['snippet']['title'],
               Subscribers = response['items'][i]['statistics']['subscriberCount'],
               Views = response['items'][i]['statistics']['viewCount'],
               Total_video = response['items'][i]['statistics']['videoCount'],
               Playlist_id = response['items'][i]['contentDetails']['relatedPlaylists']['uploads'])
    all_data.append(data)
  return all_data
  
 #store the channel statistics to a veriable   
channel_statistics = get_channel_stats(youtube, channel_ids)


channel_data = pd.DataFrame(channel_statistics)
#print(channel_data)


# print(channel_data.dtypes)
#changing the datatypes

channel_data['Subscribers'] = pd.to_numeric(channel_data['Subscribers'])
channel_data['Views'] = pd.to_numeric(channel_data['Views'])
channel_data['Total_video'] = pd.to_numeric(channel_data['Total_video'])
# print(channel_data.dtypes)

#visualization
sns.set(rc = {'figure.figsize':(12,10)})
ax = sns.barplot(x='Channel_name',y = 'Subscribers',data = channel_data)

## function to get video id

# print(channel_data)
Playlist_id = channel_data.loc[channel_data['Channel_name']=='E-Learning Bridge','Playlist_id'].iloc[0]
print(Playlist_id)

def get_video_ids(youtube,playlist_id):
  request = youtube.playlistItems().list(
    part = 'contentDetails',
    playlistId = Playlist_id,
    maxResults = 50)
  response = request.execute()

  video_ids = []
  for i in range(len((response['items']))):
    video_ids.append(response['items'][i]['contentDetails']['videoId'])

  next_page_token = response.get('nextPageToken')
  more_pages = True
  while more_pages:
    if next_page_token is None:
      more_pages = False
    else:
      request = youtube.playlistItems().list(
                  part = 'contentDetails',
                  playlistId = Playlist_id,
                  maxResults = 50,
                  pageToken = next_page_token)
      response = request.execute()

      for i in range(len((response['items']))):
        video_ids.append(response['items'][i]['contentDetails']['videoId'])

      next_page_token = response.get('nextPageToken')
      
    
    
    
  return video_ids

video_ids = get_video_ids(youtube, Playlist_id)
#print(video_ids)


#function to get video details
def get_video_details(youtube,video_ids):
  all_video_stats = []
  for i in range (0, len(video_ids),50):
    request = youtube.videos().list(
                part = 'snippet,statistics',
                id = ','.join(video_ids[i:i+50]))
    response = request.execute()

    for video in response['items']:
      video_stats = dict(Title = video['snippet']['title'],
                        published_date = video['snippet']['publishedAt'],
                        Views = video['statistics']['viewCount'],
                        Likes = video['statistics']['likeCount'],
                        # Dislikes = video['statistics']['dislikeCount'],
                        Comments = video['statistics']['commentCount'])
      all_video_stats.append(video_stats)


  
  return all_video_stats

video_detail = get_video_details(youtube, video_ids)

video_data = pd.DataFrame(video_detail)
print(video_data)
                                 


























