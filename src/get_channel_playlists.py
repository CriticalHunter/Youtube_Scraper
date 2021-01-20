import sqlite3, time

def get_channel_playlists(youtube,channel_id,single=False,playlistID=''):

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
            if (single == True and playlist['id'] == playlistID) or single == False:

                 
                Playlist_title = playlist['snippet']['title']
                Channel_Id = playlist['snippet']['channelId']
                Channel_Title = playlist['snippet']['channelTitle']
                Published_At = playlist['snippet']['publishedAt']
                Current_Video_Count = playlist['contentDetails']['itemCount']
                Playlist_Seconds = 0
                Playlist_Duration = '0'
                cur.execute("SELECT Is_Seen FROM tb_playlists WHERE Playlist_ID = ?" ,(Playlist_ID,))
                temp = cur.fetchone()
                try:
                    temp = temp[0]
                    if temp == 1:
                        Is_Seen = 1
                    else:
                        Is_Seen = 0 
                except:
                    Is_Seen = 0
                                        # 0 = not seen    1 = seen
                cur.execute("SELECT Worth FROM tb_playlists WHERE Playlist_ID = ?" ,(Playlist_ID,))
                temp = cur.fetchone()
                try:
                    temp = temp[0]
                    if temp == 1:
                        Worth = 1
                    else:
                        Worth = 0 
                except:
                    Worth = 0                        
                
                cur.execute("SELECT Downloaded_Videos FROM tb_playlists WHERE Playlist_ID = ?" ,(Playlist_ID,))
                temp = cur.fetchone()
                try:
                    temp = int(temp[0])
                    if temp > 0:
                        Downloaded_Videos = temp
                    else:
                        Downloaded_Videos = 0 
                except:
                    Downloaded_Videos = 0  
                cur.execute("SELECT Folder_Size_GB FROM tb_playlists WHERE Playlist_ID = ?" ,(Playlist_ID,))
                temp = cur.fetchone()
                try:
                    temp = int(temp[0])
                    if temp > 0:
                        Folder_Size_GB = temp
                    else:
                        Folder_Size_GB = 0 
                except:
                    Folder_Size_GB = 0  
                params = (Playlist_ID,Playlist_title,Channel_Id,Channel_Title,Published_At,Current_Video_Count,Playlist_Seconds,Playlist_Duration,Is_Seen,Worth,0,0,Downloaded_Videos,Folder_Size_GB)
                cur.execute("INSERT OR REPLACE INTO tb_playlists VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?, 0, 1)", params)
                last_time = time.time()
                cur.execute("UPDATE tb_playlists SET Playlist_last_Scraped = ? WHERE Playlist_ID = ? ",(last_time,Playlist_ID))
        if next_page_token is None:
            break
    
    playlist_ids = set(playlist_ids)
    playlist_ids = list(playlist_ids)
    count = len(playlist_ids)
    cur.execute("UPDATE tb_channels SET Playlist_Count = ? WHERE Channel_ID = ? ",(count,channel_id))

    conn.commit()                                               # Push the data into database
    conn.close()
    
    return playlist_ids

if __name__ == "__main__":
    pass