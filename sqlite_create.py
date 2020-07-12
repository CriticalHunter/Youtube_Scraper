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
        Comment_Count INTEGER,
        Subscriber_Count INTEGER,
        Video_Count INTEGER,
        Playlist_Count INTEGER
    )

        """)


    cur.execute("""CREATE TABLE IF NOT EXISTS tb_playlists(
        Playlist_ID TEXT PRIMARY KEY,
        Playlist_title TEXT,
        Channel_Id TEXT NOT NULL,
        Channel_Title TEXT NOT NULL,
        Published_At TEXT NOT NULL,
        Item_Count INTEGER,
        FOREIGN KEY (Channel_Id)
        REFERENCES tb_channels (Channel_Id)
    )
    """)

    cur.execute("""CREATE TABLE IF NOT EXISTS tb_videos (
        Video_id TEXT PRIMARY KEY,
        Video_title TEXT,
        Upload_playlistId TEXT,
        Playlist_Id TEXT,
        Published_At TEXT NOT NULL,
        Channel_Id TEXT NOT NULL,
        Channel_Title TEXT NOT NULL,
        View_Count INTEGER,
        Like_Count INTEGER,
        Dislike_Count INTEGER,
        Favorite_Count INTEGER,
        Comment_Count INTEGER,
        FOREIGN KEY (Channel_Id)
        REFERENCES tb_channels (Channel_Id),
        FOREIGN KEY (Playlist_Id)
        REFERENCES tb_playlists (Playlist_Id)
    )
    """)