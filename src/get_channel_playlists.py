import sqlite3

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
    cur.execute("UPDATE tb_channels SET Playlist_Count = ? WHERE Channel_ID = ? ",(count,channel_id))

    conn.commit()                                               # Push the data into database
    conn.close()
    
    return playlist_ids

if __name__ == "__main__":
    pass