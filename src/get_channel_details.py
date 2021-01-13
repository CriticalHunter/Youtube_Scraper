import sqlite3
from src.get_channel_playlists import get_channel_playlists
import sys

def get_channel_details(youtube,channel_id,single=False,playlistID=''):

    
    

    request = youtube.channels().list(part="snippet,statistics",
                                      id=channel_id
                                      ).execute()

    #print(request['items'][0]['snippet'])
    Channel_Id = channel_id
    try:
        Channel_title = request['items'][0]['snippet']['title']
    except:
        try:
            conn = sqlite3.connect('youtube.db')              
            cur = conn.cursor()
            cur.execute("SELECT Channel_Id from tb_channels")
            cur.execute("UPDATE tb_channels SET Is_Removed = ? WHERE Channel_ID = ? ",(1,Channel_Id))
            conn.commit()                                               # Push the data into database
            conn.close()
            sys.exit()
        except:
            print("Channel ID not valid")
            sys.exit()
    Published_At = request['items'][0]['snippet']['publishedAt']
    try:
        Country = request['items'][0]['snippet']['country']
    except:
        Country = None
    View_Count = request['items'][0]['statistics']['viewCount']

    Subscriber_Count = request['items'][0]['statistics']['subscriberCount']
    Video_Count = request['items'][0]['statistics']['videoCount']

    params = (Channel_Id,Channel_title,Published_At,Country,View_Count,Subscriber_Count,Video_Count)

    conn = sqlite3.connect('youtube.db')              
    cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO tb_channels VALUES (?, ?, ?, ?, ?, ?, ?, 0, 0, 'Scrape Entire Channel',0, 0, 0, 0, 'Never',1)", params)
    
    conn.commit()                                               # Push the data into database
    conn.close()

    get_channel_playlists(youtube,Channel_Id,single,playlistID)

if __name__ == "__main__":
    pass