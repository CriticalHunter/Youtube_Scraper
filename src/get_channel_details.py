import sqlite3
from src.get_channel_playlists import get_channel_playlists
import sys

def get_channel_details(youtube,channel_id,single=False,playlistID=''):

    
    

    request = youtube.channels().list(part="snippet,statistics",
                                      id=channel_id
                                      ).execute()

    #print(request['items'][0]['snippet'])
    print(request)
    Channel_Id = channel_id
    flag1 = True
    flag2 = True
    conn = sqlite3.connect('youtube.db')              
    cur = conn.cursor()
    try:
        Channel_title = request['items'][0]['snippet']['title']
    except:
        flag1 = False
    print(request,'2')
    try:
        cur.execute("SELECT Is_Deleted from tb_channels")
    except:
        flag2 = False
    print(request,'3')
    cur.execute("SELECT Is_Deleted from tb_channels WHERE Channel_ID = ? ",(Channel_Id,))
    flag3 = cur.fetchone()
    print(request,'4')
    if flag3 is None:
        pass
    else:
        flag3 = flag3[0]
    if flag1 == False and flag2 == False:
        print("Channel ID not valid")
        sys.exit()
    if flag1 == False and flag2 == True and flag3 == 1:
        print("Channel is Deleted")
        conn.commit()                                               # Push the data into database
        conn.close()
        sys.exit()
    if flag1 == False and flag2 == True and flag3 == 0:
        cur.execute("SELECT Channel_Id from tb_channels")
        cur.execute("UPDATE tb_channels SET Is_Deleted = ? WHERE Channel_ID = ? ",(1,Channel_Id))
        print("Channel is Deleted")
        conn.commit()                                               # Push the data into database
        conn.close()
        sys.exit()
    
    Description = request['items'][0]['snippet']['description']
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
    cur.execute("INSERT OR REPLACE INTO tb_channels VALUES (?, ?, ?, ?, ?, ?, ?, 0, 0, 'First, Scrape Entire Channel',0, 0, 0, 0, 'Never',1,'')", params)
    cur.execute("UPDATE tb_channels SET Description = ? WHERE Channel_ID = ? ",(Description,Channel_Id))
    conn.commit()                                               # Push the data into database
    conn.close()

    get_channel_playlists(youtube,Channel_Id,single,playlistID)

if __name__ == "__main__":
    pass