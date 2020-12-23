#https://developers.google.com/youtube/v3/docs
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import sqlite3, time
from bs4 import BeautifulSoup

global count1
global api_key, youtube
count1 = 0

'''
To run any function(s), first run get_api_key, to start the Youtube API
'''
def create_new():
    conn = sqlite3.connect('youtube.db')              
    cur = conn.cursor() 


    cur.execute("""CREATE TABLE IF NOT EXISTS tb_channels (
        Channel_ID TEXT PRIMARY KEY,
        Channel_title TEXT,
        Published_At TEXT NOT NULL,
        Country TEXT,
        View_Count INTEGER,
        Subscriber_Count INTEGER,
        Video_Count INTEGER,
        Playlist_Count INTEGER
    )

        """)


    cur.execute("""CREATE TABLE IF NOT EXISTS tb_playlists(
        Playlist_ID TEXT PRIMARY KEY,
        Playlist_title TEXT,
        Channel_ID TEXT NOT NULL,
        Channel_Title TEXT NOT NULL,
        Published_At TEXT NOT NULL,
        Item_Count INTEGER,
        Playlist_Seconds INTEGER,
        Playlist_Duration TEXT,
        Is_Seen INTEGER,
        Worth INTEGER,
        FOREIGN KEY (Channel_ID)
        REFERENCES tb_channels (Channel_ID)
    )
    """)

    cur.execute("""CREATE TABLE IF NOT EXISTS tb_videos (
        Video_ID TEXT PRIMARY KEY,
        Video_title TEXT,
        Is_Seen INTEGER,
        Worth INTEGER,
        Upload_playlistId TEXT,
        Playlist_ID TEXT,
        Published_At TEXT NOT NULL,
        epoch REAL NOT NULL,
        Channel_ID TEXT NOT NULL,
        Channel_Title TEXT NOT NULL,
        View_Count INTEGER,
        Like_Count INTEGER,
        Dislike_Count INTEGER,
        Upvote_Ratio REAL,
        Comment_Count INTEGER,
        Duration TEXT,
        video_seconds INTEGER,
        Is_Licensed INTEGER,
        Is_Deleted INTEGER,
        FOREIGN KEY (Channel_ID)
        REFERENCES tb_channels (Channel_ID),
        FOREIGN KEY (Playlist_ID)
        REFERENCES tb_playlists (Playlist_ID)
    )
    """)

    cur.execute("""CREATE TABLE IF NOT EXISTS video_history (
        Video_ID TEXT NOT NULL,
        Watched_at TEXT ,
        epoch REAL NOT NULL,
        Is_in_Main INTEGER,
        PRIMARY KEY ( Video_ID, epoch),
        FOREIGN KEY (Video_ID)
        REFERENCES tb_videos (Video_ID)
    )

        """)
        
def get_api_key(key):
    
    global api_key,youtube
    api_key = key
    youtube = build('youtube','v3',developerKey=api_key)

get_api_key('AIzaSyBSumleKJ1eLSsTcMxXH2szgB_OCOXnslg')


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



'''
Increasingly, searching by channel name returns None. Prefer search by ID
'''
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
            sub_count = str(sub_count) + ' Subscribers'
        ch_id = response['items'][0]['id']
        
        print(" ")
        print(sub_count)
        return ch_id
    except KeyError:
        print(" ")
        print("          Error : Channel not Found ")
        print(" ")




def get_videos_stats(video_ids,flag,playlistID = None):
    global youtube
    conn = sqlite3.connect('youtube.db')              
    cur = conn.cursor()
    count1 = 0
    stats = []
    tot_len = 0

    for i in range(0, len(video_ids), 50):
        res = youtube.videos().list(id=','.join(video_ids[i:i+50]),
                                   part='snippet,statistics,contentDetails').execute()
        stats += res['items']
    

    for video in stats:
        count1 += 1

        Video_id = video['id']
        Video_title = video['snippet']['title']
        Upload_playlistId = video['snippet']['channelId']
        
        try:
            Playlist_Id = video['snippet']['playlistId']
        except:
            Playlist_Id = playlistID                                    # When call is grom a playlist
            
        Published_At = video['snippet']['publishedAt']
        date_format = "%Y-%m-%dT%H:%M:%SZ" 
        epoch = float(time.mktime(time.strptime(Published_At, date_format)))
        Channel_Id = video['snippet']['channelId']
        Channel_Title = video['snippet']['channelTitle']
        try:
            View_Count = video['statistics']['viewCount']
        except:
            View_Count = 0
            flag = 2
        try:
            Like_Count = video['statistics']['likeCount']
        except:
            Like_Count = 0
        try:
            Dislike_Count = video['statistics']['dislikeCount']
        except:
            Dislike_Count = 0
        try:
            Upvote_Ratio = (int(Like_Count)/(int(Like_Count)+(int(Dislike_Count))))*100
        except:
            Upvote_Ratio = 0
        try:
            Comment_Count = video['statistics']['commentCount']
        except:            
            Comment_Count = 0
        try:
            Duration = str(video['contentDetails']['duration'])
            Duration = Duration.replace('PT','')
            hh=mm=ss = '00'
            if Duration.find('H') != -1:
                hh = Duration.split('H')[0]
                temp = hh+'H'
                if len(hh) == 1:
                    hh = '0'+hh
                Duration = Duration.replace(temp,'')
            if Duration.find('M') != -1:
                mm = Duration.split('M')[0]
                temp = mm+'M'
                if len(mm) == 1:
                    mm = '0'+mm
                Duration = Duration.replace(temp,'')
            if Duration.find('S') != -1:
                ss = Duration.split('S')[0]
                if len(ss) == 1:
                    ss = '0'+ss
            Duration = (hh+':'+mm+':'+ss)
            video_seconds = timedelta(hours = int(hh),
                            minutes= int(mm),
                            seconds= int(ss)).total_seconds()
            if playlistID is not None:
                tot_len += video_seconds
        except:            
            Duration = '0'
            video_seconds = 0
            flag = 2
            
        try:
            Is_Licensed = video['contentDetails']['licensedContent']
        except:            
            Is_Licensed = 0 
        Is_Seen = 0                     # 0 = not seen    1 = seen
        Worth = 0                       # 0 = not rated , ratings = 1(not worth saving)/2(worth saving)
        Is_Deleted = 0
        params = (Video_id,Video_title,Is_Seen,Worth,Upload_playlistId,Playlist_Id,Published_At,epoch,Channel_Id,Channel_Title,View_Count,Like_Count,Dislike_Count,Upvote_Ratio,Comment_Count,Duration,video_seconds,Is_Licensed,Is_Deleted)
        if flag == 1:
            cur.execute("INSERT OR REPLACE INTO tb_videos VALUES (?, ?, ?, ?, ?, ?, ? ,? ,? ,? ,? ,? , ?, ?, ?, ?, ?, ?, ?)", params)
        else:
            cur.execute("INSERT OR IGNORE INTO tb_videos VALUES (?, ?, ?, ?, ?, ?, ? ,? ,? ,? ,? ,? , ?, ?, ?, ?, ?, ?, ?)", params)

    conn.commit()                                               # Push the data into database
    conn.close()
    if tot_len > 0:
        return tot_len


def get_channel_playlists(channel_id):
    global youtube
    conn = sqlite3.connect('youtube.db')              
    cur = conn.cursor()
    
    playlists = []
    playlist_ids = []
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

            Playlist_ID = playlist['id']                    ;   playlist_ids.append(Playlist_ID) 
            Playlist_title = playlist['snippet']['title']
            Channel_Id = playlist['snippet']['channelId']
            Channel_Title = playlist['snippet']['channelTitle']
            Published_At = playlist['snippet']['publishedAt']
            Item_Count = playlist['contentDetails']['itemCount']
            Playlist_Seconds = 0
            Playlist_Duration = '0'
            Is_Seen = 0                     # 0 = not seen    1 = seen
            Worth = 0                       # 0 = not rated , ratings = 1(not worth saving)/2(worth saving)
            params = (Playlist_ID,Playlist_title,Channel_Id,Channel_Title,Published_At,Item_Count,Playlist_Seconds,Playlist_Duration,Is_Seen,Worth)
            cur.execute("INSERT OR REPLACE INTO tb_playlists VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", params)
        if next_page_token is None:
            break
    
    playlist_ids = set(playlist_ids)
    playlist_ids = list(playlist_ids)
    count = len(playlist_ids)
    cur.execute("UPDATE tb_channels SET Playlist_Count = ? WHERE Channel_ID = ? ",(count,Channel_Id))

    conn.commit()                                               # Push the data into database
    conn.close()
    
    return playlist_ids

''' get_channel_details() and  entire_channel(ch_id) use  get_channel_playlists '''
def get_channel_details(channel_id):
    global youtube
    conn = sqlite3.connect('youtube.db')              
    cur = conn.cursor()
    

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

    Subscriber_Count = request['items'][0]['statistics']['subscriberCount']
    Video_Count = request['items'][0]['statistics']['videoCount']

    params = (Channel_Id,Channel_title,Published_At,Country,View_Count,Subscriber_Count,Video_Count)

    cur.execute("INSERT OR REPLACE INTO tb_channels VALUES (?, ?, ?, ?, ?, ?, ?, 0)", params)
    
    conn.commit()                                               # Push the data into database
    conn.close()

    get_channel_playlists(Channel_Id)





''' get_playlist_videos(playlistID) takes only a single Playlist ID as string  '''
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
            cur.execute("INSERT OR IGNORE INTO tb_videos VALUES (?, ?, ?, ?, ?, ?, ?, 0,0,0,0,0,'',0,0,0,0)", params)    

        
    print('Videos in this playlist =',len(video_IDS))
    conn.commit()                                               # Push the data into database
    conn.close()
    
    Playlist_Seconds = get_videos_stats(video_IDS,1,playlistID)
    Playlist_Duration = str(timedelta(seconds = Playlist_Seconds))
    conn = sqlite3.connect('youtube.db')              
    cur = conn.cursor()
    cur.execute("UPDATE tb_playlists SET Playlist_Seconds = ? WHERE playlist_ID = ? ",(Playlist_Seconds,playlistID))
    cur.execute("UPDATE tb_playlists SET Playlist_Duration = ? WHERE playlist_ID = ? ",(Playlist_Duration,playlistID))
    conn.commit()                                               # Push the data into database
    conn.close()
    




def get_channel_videos(channel_id):
    global youtube
    conn = sqlite3.connect('youtube.db')              
    cur = conn.cursor()

    res = youtube.channels().list(id=channel_id, 
                                  part='contentDetails').execute()
    
    playlist_id = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    
    videos = []
    next_page_token = None
    new_video_ids = []

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

    for newVid in video_ids:
        cur.execute("SELECT Video_id FROM tb_videos WHERE Video_id=?",(newVid,))
        if cur.fetchone():
            pass
        else:
            new_video_ids.append(newVid)
    conn.commit()                                               # Push the data into database
    conn.close()

    print('\nParsing ',len(new_video_ids),' videos, which are not in any playlist')
    get_videos_stats(video_ids,flag=0)

def load_history():
    count_loc_prog = 0
    with open("takeout/history/watch-history.html",encoding='utf-8') as fp:
        conn = sqlite3.connect('youtube.db')              
        cur = conn.cursor()

        soup = BeautifulSoup(fp,'lxml')
        soup = soup.body

        videos = soup.find_all("div", {"class": "content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1"})

        print(len(videos))
        
        for video in videos:
            count_loc_prog += 1
            if count_loc_prog % 500 == 0:
                print(count_loc_prog)
            tags = video.find_all('a')
            # try:

            if tags == []:
                continue
            
            V_link = tags[0].get('href')
            V_link = V_link.split('=')[-1]
            br_tags = video.find_all('br')
            for tag in br_tags:
                watched_at = str(tag.next_sibling)
                if watched_at[-3:-1] == 'IS':
                    final_time = (watched_at)
                    temp = final_time.replace('IST','+0530')
                    epoch = time.mktime(time.strptime(temp, "%b %d, %Y, %H:%M:%S %p %z"))
            cur.execute("INSERT OR IGNORE INTO video_history VALUES (?,?,?,?)", (V_link,final_time,epoch,0))
               
            # except:

            #     continue
            

        conn.commit()                                               # Push the data into database
        conn.close()

    def freq():
        conn = sqlite3.connect('youtube.db')              
        cur = conn.cursor()

        

load_history()

def entire_channel(ch_id):
    get_channel_details(ch_id)
    playlists_list = get_channel_playlists(ch_id)
    count = 0
    print('\nThere are ',len(playlists_list),' original/imported playlists\n')
    for playlist in playlists_list:
        count += 1
        print('\nParsing playlist ',count)
        get_playlist_videos(playlist)
        
        count1 = 0
    get_channel_videos(ch_id)

# entire_channel('UCJQJ4GjTiq5lmn8czf8oo0Q')
def just_playlist(playlist_id):
    get_playlist_videos(playlist_id)

