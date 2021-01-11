import sqlite3
from src.get_channel_playlists import get_channel_playlists

def get_channel_details(youtube,channel_id,single=False,playlistID=''):

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

    get_channel_playlists(youtube,Channel_Id,single,playlistID)

if __name__ == "__main__":
    pass