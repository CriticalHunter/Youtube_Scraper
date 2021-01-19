import sqlite3
from datetime import timedelta

from src.get_video_stats import get_videos_stats
from src.get_channel_details import get_channel_details

def get_playlist_videos(youtube,playlistID,ec=False,ch_id=None):

    ch_ID = 'skip'
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
            try:
                ch_ID = video['snippet']['channelId']
            except:
                ch_ID = 'skip'
            if ec == True:
                params = (Video_id,"",0,0,ch_id,None,None,0,ch_id,'',0,0,0,0,0,'',0,0,1,0)
                cur.execute("INSERT OR IGNORE INTO tb_videos VALUES (?, ?, ?,? ,?, ?, ?, ?,?, ?,?,?,?,?,?,?,?,?,?,?)", params)
            else:
                params = (Video_id,"",0,0,"","","")
                cur.execute("INSERT OR IGNORE INTO tb_videos VALUES (?, ?, ?,? ,?, ?, ?, 0,'', '',0,0,0,0,0,'',0,0,0,0)", params)    

        
    print('Videos in this playlist =',len(video_IDS))
    conn.commit()                                               # Push the data into database
    conn.close()
    
    if ch_ID == 'skip':
        return 0
    else:
        if ec == False:
            get_channel_details(youtube,ch_ID,True,playlistID)

        Playlist_Seconds = get_videos_stats(youtube,video_IDS,1,playlistID)
        Playlist_Duration = str(timedelta(seconds = Playlist_Seconds))
        conn = sqlite3.connect('youtube.db')              
        cur = conn.cursor()
        cur.execute("UPDATE tb_playlists SET Playlist_Seconds = ? WHERE playlist_ID = ? ",(Playlist_Seconds,playlistID))
        cur.execute("UPDATE tb_playlists SET Playlist_Duration = ? WHERE playlist_ID = ? ",(Playlist_Duration,playlistID))
        conn.commit()                                               # Push the data into database
        conn.close()

if __name__ == "__main__":
    pass