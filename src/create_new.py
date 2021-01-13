import sqlite3

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
        Is_Downloaded INTEGER,
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
    
    cur.execute("""CREATE TABLE IF NOT EXISTS yt_downloaded (
        Video_ID TEXT PRIMARY KEY,
        Resolution TEXT,
        Raw_Size INTEGER,
        Size TEXT,
        FPS TEXT,
        bitrate,
        Audio_Type TEXT,
        Frequency INTEGER,
        Channels TEXT,
        IsInMain INTEGER,
        FOREIGN KEY (Video_ID)
        REFERENCES tb_videos (Video_ID)
    )

        """)

if __name__ == "__main__":
    create_new()