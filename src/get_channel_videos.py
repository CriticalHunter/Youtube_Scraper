import sqlite3

from src.get_video_stats import get_videos_stats

def get_channel_videos(youtube,channel_id):
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
    get_videos_stats(youtube,video_ids,flag=0)

if __name__ == "__main__":
    pass    

