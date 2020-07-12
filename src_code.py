#https://developers.google.com/youtube/v3/docs
from googleapiclient.discovery import build
from datetime import datetime

import sqlite3
global count1
global api_key, youtube

count1 = 0


def get_api_key(key):
    
    global api_key,youtube
    api_key = key
    youtube = build('youtube','v3',developerKey=api_key)



def oldest_videos_on_a_topic(topic):
    global youtube
    start_time = datetime(year=2005, month=1, day=1).strftime('%Y-%m-%dT%H:%M:%SZ')
    end_time = datetime(year=2008, month=1, day=1).strftime('%Y-%m-%dT%H:%M:%SZ')

    res = youtube.search().list(part='snippet',
                            q=topic,
                            type='video',
                            publishedAfter=start_time,
                            publishedBefore=end_time,
                            maxResults=15).execute()
    for item in sorted(res['items'], key=lambda x:x['snippet']['publishedAt']):
        print(item['snippet']['title'], item['snippet']['publishedAt'], item['id']['videoId'])
    #print(res)

def get_channel_id(ch_name):
    global youtube
    request = youtube.channels().list(
            part="snippet,contentDetails,statistics",
            forUsername=ch_name
        )
    response = request.execute()
    try:
        sub_count = int(response['items'][0]['statistics']['subscriberCount'])
        if sub_count > 1000000:
            sub_count = str(sub_count / 1000000)
            sub_count = sub_count + 'M Subscribers'
        elif sub_count > 1000:
            sub_count = str(sub_count / 1000)
            sub_count = sub_count + 'K Subscribers'
        else:
            sub_count = sub_count + ' Subscribers'
        ch_id = response['items'][0]['id']
        print(sub_count)
        return ch_id
    except KeyError:
        print(" ")
        print("          Error : Channel not Found ")
        print(" ")



def get_videos_stats(video_ids,playlistID = None):
    global youtube
    conn = sqlite3.connect('youtube.db')              
    cur = conn.cursor()
    count1 = 0

    stats = []
    for i in range(0, len(video_ids), 50):
        res = youtube.videos().list(id=','.join(video_ids[i:i+50]),
                                   part='snippet,statistics').execute()
        stats += res['items']
    

    for video in stats:
        count1 += 1

        Video_id = video['id']
        Video_title = video['snippet']['title']
        Upload_playlistId = video['snippet']['channelId']
        try:
            Playlist_Id = video['snippet']['playlistId']
        except:
            Playlist_Id = playlistID
        Published_At = video['snippet']['publishedAt']
        Channel_Id = video['snippet']['channelId']
        Channel_Title = video['snippet']['channelTitle']
        try:
            View_Count = video['statistics']['viewCount']
        except:
            View_Count = 0
        try:
            Like_Count = video['statistics']['likeCount']
        except:
            Like_Count = 0
        try:
            Dislike_Count = video['statistics']['dislikeCount']
        except:
            Dislike_Count = 0
        try:
            Favorite_Count = video['statistics']['favoriteCount']
        except:
            Favorite_Count = 0
        try:
            Comment_Count = video['statistics']['commentCount']
        except:            
            Comment_Count = 0
            
        params = (Video_id,Video_title,Upload_playlistId,Playlist_Id,Published_At,Channel_Id,Channel_Title,View_Count,Like_Count,Dislike_Count,Favorite_Count,Comment_Count)
        cur.execute("INSERT OR REPLACE INTO tb_videos VALUES (?, ?, ?, ?, ?, ?, ?, ? ,? ,? ,? ,? )", params)

    conn.commit()                                               # Push the data into database
    conn.close()

def get_channel_details(channel_id):
    global youtube
    conn = sqlite3.connect('youtube.db')              
    cur = conn.cursor()
    
    print(api_key)
    request = youtube.channels().list(part="snippet,statistics",
                                      id=channel_id
                                      ).execute()

    #print(request['items'][0]['snippet'])

    Channel_Id = channel_id
    Channel_title = request['items'][0]['snippet']['title']
    Published_At = request['items'][0]['snippet']['publishedAt']
    try:
        Country = request['items'][0]['snippet']['country']
    except:
        Country = None
    View_Count = request['items'][0]['statistics']['viewCount']
    Comment_Count = request['items'][0]['statistics']['commentCount']
    Subscriber_Count = request['items'][0]['statistics']['subscriberCount']
    Video_Count = request['items'][0]['statistics']['videoCount']

    params = (Channel_Id,Channel_title,Published_At,Country,View_Count,Comment_Count,Subscriber_Count,Video_Count)

    cur.execute("INSERT OR REPLACE INTO tb_channels VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0)", params)
    
    conn.commit()                                               # Push the data into database
    conn.close()

def get_playlist_videos(playlistID):
    global youtube
    conn = sqlite3.connect('youtube.db')              
    cur = conn.cursor()

    videos = []
    next_page_token = None
    video_IDS = []
    while 1:
        res = youtube.playlistItems().list(part="snippet",
                                                maxResults=50,
                                                playlistId=playlistID,
                                                pageToken=next_page_token
                                            ).execute()
        videos += res['items']
        next_page_token = res.get('nextPageToken')
        
        if next_page_token is None:
            break
    

    for video in videos:
            
            Video_id = video['snippet']['resourceId']['videoId'];   video_IDS.append(Video_id)

            params = (Video_id,"","","","","","")
            cur.execute("INSERT OR IGNORE INTO tb_videos VALUES (?, ?, ?, ?, ?, ?, ?, 0,0,0,0,0)", params)    

        
    print('Videos in this playlist =',len(video_IDS))
    conn.commit()                                               # Push the data into database
    conn.close()
    
    get_videos_stats(video_IDS,playlistID)

    

def get_channel_playlists(channel_id):
    global youtube
    conn = sqlite3.connect('youtube.db')              
    cur = conn.cursor()
    
    playlists = []
    playlist_ids = []
    count = 0
    next_page_token = None
    
    while 1:
        res = youtube.playlists().list( part="snippet,contentDetails",
                                        channelId=channel_id,
                                        pageToken=next_page_token,
                                        maxResults=50
                                    ).execute()
        playlists += res['items']
        next_page_token = res.get('nextPageToken')
        

        for playlist in playlists:
            count += 1

            Playlist_ID = playlist['id']                    ;   playlist_ids.append(Playlist_ID) 
            Playlist_title = playlist['snippet']['title']
            Channel_Id = playlist['snippet']['channelId']
            Channel_Title = playlist['snippet']['channelTitle']
            Published_At = playlist['snippet']['publishedAt']
            Item_Count = playlist['contentDetails']['itemCount']
            params = (Playlist_ID,Playlist_title,Channel_Id,Channel_Title,Published_At,Item_Count)
            cur.execute("INSERT OR REPLACE INTO tb_playlists VALUES (?, ?, ?, ?, ?, ?)", params)
        if next_page_token is None:
            break
    
    cur.execute("UPDATE tb_channels SET Playlist_Count = ? WHERE Channel_ID = ? ",(count,Channel_Id))

    


    conn.commit()                                               # Push the data into database
    conn.close()
    return playlist_ids



def get_channel_videos(channel_id):
    global youtube
    
    res = youtube.channels().list(id=channel_id, 
                                  part='contentDetails').execute()
    
    playlist_id = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    
    videos = []
    next_page_token = None
    
    while 1:
        res = youtube.playlistItems().list(playlistId=playlist_id, 
                                           part='snippet', 
                                           maxResults=50,
                                           pageToken=next_page_token).execute()
        videos += res['items']
        next_page_token = res.get('nextPageToken')
        
    
        video_ids = list(map(lambda x:x['snippet']['resourceId']['videoId'], videos))

        if next_page_token is None:
            break

    print('Parsing ',len(video_ids),' videos, which are not in playlist')
    get_videos_stats(video_ids)



def entire_channel(ch_id):
    get_channel_details(ch_id)
    playlists_list = get_channel_playlists(ch_id)
    count = 0
    print('There are ',len(playlists_list),' original/imported playlists')
    for playlist in playlists_list:
        count += 1
        get_playlist_videos(playlist)
        print('Parsing playlist ',count)
        count1 = 0
    get_channel_videos(ch_id)

def just_playlist(playlist_id):
    get_playlist_videos(playlist_id)
