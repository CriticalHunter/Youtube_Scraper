import sqlite3
import os

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
        Playlist_Count INTEGER,
        Channel_Duration INTEGER,
        Duration_in_Text TEXT,
        Is_Removed INTEGER,
        Deleted_Videos INTEGER,
        Downloaded_Videos INTEGER,
        Folder_Size_GB INTEGER,
        Channel_last_Scraped TEXT,
        Auto_Update INTEGER
    )

        """)


    cur.execute("""CREATE TABLE IF NOT EXISTS tb_playlists(
        Playlist_ID TEXT PRIMARY KEY,
        Playlist_title TEXT,
        Channel_ID TEXT NOT NULL,
        Channel_Title TEXT NOT NULL,
        Published_At TEXT NOT NULL,
        Current_Video_Count INTEGER,
        Playlist_Seconds INTEGER,
        Playlist_Duration TEXT,
        Is_Seen INTEGER,
        Worth INTEGER,
        Is_Removed INTEGER,
        Deleted_Videos INTEGER,
        Downloaded_Videos INTEGER,
        Folder_Size_GB INTEGER,
        Playlist_last_Scraped TEXT,
        Auto_Update INTEGER
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
        Is_Downloaded INTEGER
    )
    """)

    cur.execute("""CREATE TABLE IF NOT EXISTS video_history (
        Video_ID TEXT NOT NULL,
        Watched_at TEXT ,
        epoch REAL NOT NULL,
        Is_in_Main INTEGER,
        PRIMARY KEY ( Video_ID, epoch)
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
        IsInMain INTEGER
    )

        """)
    
    conn.commit()                                               # Push the data into database
    conn.close()

def migrate():
    conn = sqlite3.connect('youtube.db')              
    cur = conn.cursor() 

    cur.execute("PRAGMA foreign_keys=off")
    cur.execute("BEGIN TRANSACTION")
    cur.execute("ALTER TABLE tb_channels RENAME TO _tb_channels_old")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tb_channels (
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
    cur.execute("INSERT INTO tb_channels SELECT * FROM _tb_channels_old")
    try:
        cur.execute("ALTER TABLE tb_channels ADD COLUMN Channel_Duration INTEGER")
        cur.execute("ALTER TABLE tb_channels ADD COLUMN Duration_in_Text TEXT")
        cur.execute("ALTER TABLE tb_channels ADD COLUMN Is_Removed INTEGER")
        cur.execute("ALTER TABLE tb_channels ADD COLUMN Deleted_Videos INTEGER")
        cur.execute("ALTER TABLE tb_channels ADD COLUMN Downloaded_Videos INTEGER")
        cur.execute("ALTER TABLE tb_channels ADD COLUMN Folder_Size_GB INTEGER")
        cur.execute("ALTER TABLE tb_channels ADD COLUMN Channel_last_Scraped TEXT")
        cur.execute("ALTER TABLE tb_channels ADD COLUMN Auto_Update INTEGER")
    except:
        # These stats are added after intitial release of this code.
        pass
    cur.execute("DROP TABLE _tb_channels_old")

    cur.execute("ALTER TABLE tb_playlists RENAME TO _tb_playlists_old")
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
        Worth INTEGER
    )
    """)
    cur.execute("INSERT INTO tb_playlists SELECT * FROM _tb_playlists_old")
    try:
        cur.execute("ALTER TABLE tb_playlists ADD COLUMN Is_Removed INTEGER")
        cur.execute("ALTER TABLE tb_playlists ADD COLUMN Deleted_Videos INTEGER")
        cur.execute("ALTER TABLE tb_playlists ADD COLUMN Downloaded_Videos INTEGER")
        cur.execute("ALTER TABLE tb_playlists ADD COLUMN Folder_Size_GB INTEGER")
        cur.execute("ALTER TABLE tb_playlists ADD COLUMN Playlist_last_Scraped TEXT")
        cur.execute("ALTER TABLE tb_playlists ADD COLUMN Auto_Update INTEGER")
        cur.execute("ALTER TABLE tb_playlists RENAME COLUMN Item_Count TO Current_Video_Count")
    except:
        # These stats are added after intitial release of this code.
        pass
    cur.execute("DROP TABLE _tb_playlists_old")

    cur.execute("ALTER TABLE tb_videos RENAME TO _tb_videos_old")
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
        Is_Downloaded INTEGER
    )
    """)
    cur.execute("INSERT INTO tb_videos SELECT * FROM _tb_videos_old") 
    cur.execute("DROP TABLE _tb_videos_old")

    
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
        Is_In_Main INTEGER
    )

        """)
    try:
        cur.execute("DROP TABLE tb_downloaded")
    except:
        pass
    cur.execute("PRAGMA foreign_keys=on")
    conn.commit()                                               # Push the data into database
    conn.close()

def dbase():
    if not os.path.exists("youtube.db"):
        create_new()
    else:
        conn = sqlite3.connect('youtube.db')              
        cur = conn.cursor() 
        try:
            cur.execute("SELECT Deleted_Videos FROM tb_channels")
        except:
            migrate()

        
if __name__ == "__main__":
    dbase()