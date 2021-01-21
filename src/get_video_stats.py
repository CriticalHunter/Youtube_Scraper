from datetime import timedelta
import sqlite3, time
from os import path
import sys

def get_videos_stats(youtube,video_ids,flag=1,playlistID = None):
    oflag = flag
    if not path.exists('youtube.db'):
        print("Please Create the database First")
        sys.exit()
    else:
        pass

    conn = sqlite3.connect('youtube.db')              
    cur = conn.cursor()
    count1 = 0
    stats = []
    tot_len = 0
    for i in range(0, len(video_ids), 50):
        res = youtube.videos().list(id=','.join(video_ids[i:i+50]),
                                   part='snippet,statistics,contentDetails').execute()
        stats += res['items']
    
    new_ids = []
    for video in stats:
        count1 += 1
        try:
            Video_id = video['id']
        except:
            Video_id = ''
            flag = 3
        new_ids.append(Video_id)
        Video_title = video['snippet']['title']
        Upload_playlistId = video['snippet']['channelId']
        
        if playlistID is not None:
            Playlist_Id = playlistID                                    # When call is from a playlist
        else:
            cur.execute("SELECT Playlist_ID FROM tb_videos WHERE Video_ID = ?" ,(Video_id,))
            result = cur.fetchone()
            if result is None:
                Playlist_Id = None
            else:
                if type(result) is tuple:
                    Playlist_Id = result[0]
                elif type(result) is str:
                    Playlist_Id = result
                else:
                    Playlist_Id = None
        Published_At = video['snippet']['publishedAt']
        date_format = "%Y-%m-%dT%H:%M:%SZ" 
        epoch = float(time.mktime(time.strptime(Published_At, date_format)))
        Channel_Id = video['snippet']['channelId']
        Channel_Title = video['snippet']['channelTitle']
        try:
            View_Count = video['statistics']['viewCount']
        except:
            View_Count = 1111
        cur.execute("SELECT View_Count FROM tb_videos WHERE Video_ID = ?" ,(Video_id,))
        temp = cur.fetchone()
        try:
            temp = temp[0]
            if View_Count < temp:
                continue
        except:
            pass
        try:
            Like_Count = video['statistics']['likeCount']
        except:
            Like_Count = 0
        try:
            Dislike_Count = video['statistics']['dislikeCount']
        except:
            Dislike_Count = 0
        try:
            Upvote_Ratio = (int(Like_Count)/(int(Like_Count)+(int(Dislike_Count))))*100
        except:
            Upvote_Ratio = 0
        try:
            Comment_Count = video['statistics']['commentCount']
        except:            
            Comment_Count = 0
        try:
            Duration = str(video['contentDetails']['duration'])
            Duration = Duration.replace('PT','')
            hh=mm=ss = '00'
            if Duration.find('H') != -1:
                hh = Duration.split('H')[0]
                temp = hh+'H'
                if len(hh) == 1:
                    hh = '0'+hh
                Duration = Duration.replace(temp,'')
            if Duration.find('M') != -1:
                mm = Duration.split('M')[0]
                temp = mm+'M'
                if len(mm) == 1:
                    mm = '0'+mm
                Duration = Duration.replace(temp,'')
            if Duration.find('S') != -1:
                ss = Duration.split('S')[0]
                if len(ss) == 1:
                    ss = '0'+ss
            Duration = (hh+':'+mm+':'+ss)
            video_seconds = timedelta(hours = int(hh),
                            minutes= int(mm),
                            seconds= int(ss)).total_seconds()
            # if playlistID is not None:
            tot_len += video_seconds
        except:            
            Duration = '0'
            video_seconds = 0
            
        try:
            Is_Licensed = video['contentDetails']['licensedContent']
        except:            
            Is_Licensed = 0 
        cur.execute("SELECT Is_Seen FROM tb_videos WHERE Video_ID = ?" ,(Video_id,))
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
        cur.execute("SELECT Worth FROM tb_videos WHERE Video_ID = ?" ,(Video_id,))
        temp = cur.fetchone()
        try:
            temp = temp[0]
            if temp == 1:
                Worth = 1
            else:
                Worth = 0 
        except:
            Worth = 0      

        cur.execute("SELECT Is_Downloaded FROM tb_videos WHERE Video_ID = ?" ,(Video_id,))
        temp = cur.fetchone()
        try:
            temp = temp[0]
            if temp == 1:
                Is_Downloaded = 1
            else:
                Is_Downloaded = 0 
        except:
            Is_Downloaded = 0 
        Is_Deleted = 0
        if flag == 1 or flag == 2:
            Is_Deleted = 0
        elif flag == 3:
            Is_Deleted = 1
            print(Video_id,' is deleted')
            cur.execute("UPDATE tb_videos SET IS_Deleted = 1 WHERE Video_ID = ?",(Video_id,))
            flag = oflag
        params = (Video_id,Video_title,Is_Seen,Worth,Upload_playlistId,Playlist_Id,Published_At,epoch,Channel_Id,Channel_Title,View_Count,Like_Count,Dislike_Count,Upvote_Ratio,Comment_Count,Duration,video_seconds,Is_Licensed,Is_Deleted,Is_Downloaded)
        if flag == 1:
            cur.execute("INSERT OR REPLACE INTO tb_videos VALUES (?, ?, ?, ?, ?, ?, ? ,? ,? ,? ,? ,? , ?, ?, ?, ?, ?, ?, ?, ?)", params)
        elif flag == 2:
            cur.execute("INSERT OR IGNORE INTO tb_videos VALUES (?, ?, ?, ?, ?, ?, ? ,? ,? ,? ,? ,? , ?, ?, ?, ?, ?, ?, ?, ?)", params)
    conn.commit()                                               
    conn.close()

    video_ids = set(video_ids)
    new_ids = set(new_ids)
    num_new = len(new_ids)
    diff = video_ids-new_ids
    if len(diff) > 0:
        conn = sqlite3.connect('youtube.db')              
        cur = conn.cursor()
        for item in diff:
            print(item,' not available')
            try:
                params = (item,'Not Available',0,0,'','','','',Channel_Id,Channel_Title,'','','','','','','','',1,0)
                cur.execute("INSERT OR IGNORE INTO tb_videos VALUES (?, ?, ?, ?, ?, ?, ? ,? ,? ,? ,? ,? , ?, ?, ?, ?, ?, ?, ?, ?)", params)
                cur.execute("UPDATE tb_videos SET IS_Deleted = 1 WHERE Video_ID = ?",(item,))
            except:
                pass
        conn.commit()                                               
        conn.close()
    if tot_len > 0:
        return tot_len,num_new

if __name__ == "__main__":
    pass