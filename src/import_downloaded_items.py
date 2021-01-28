from pathlib import Path
import subprocess, os,re
#SELECT * FROM tb_videos WHERE Video_ID IN (SELECT Video_ID FROM yt_downloaded) ORDER BY Is_Seen
# Sanity Check
from os import listdir
from os.path import isfile, join
import sqlite3

from get_api_key import api_key
from get_video_stats import get_videos_stats

def update_local(vid_path):
    vid_path1 = '"'+vid_path+'"'
    command = "./ffmpeg -i "+vid_path1+" -hide_banner"
    try:
        with open('log1.txt', "w",encoding='utf-8') as outfile:
            subprocess.run(command, stderr=subprocess.STDOUT,stdout=outfile)
    except Exception as e:
        print(e)
    with open('log1.txt', "r",encoding='utf-8') as fhand:
        for line in fhand:
            line=line.lstrip()
            temp_match = line[0:11]
            if temp_match == 'Stream #0:0':
                result = re.findall('\d+x\d+', line)
                Resolution = result[0]
                result = re.findall('[0-9.]+ fps', line)
                try:
                    fps = result[0]
                    fps = fps.strip(' fps')
                except:
                    fps = 0
            if line.startswith('Duration:'):
                result = re.findall('\d+ ', line)
                bitrate = result[0]
            if line.startswith('Stream #0:1'):
                result = re.findall('Audio: [a-zA-Z]+,', line)
                temp = result[0]
                Audio_Type = temp.strip(',')
                Audio_Type = Audio_Type[7:]
                result = re.findall('\d+ Hz', line)
                temp = result[0]
                Frequency = temp.strip(' Hz')
                result = re.findall('Hz, \w+,', line)
                temp = result[0]
                Channels = temp.strip('Hz ,')
        raw_size = Path(vid_path).stat().st_size
        size = raw_size/(1024*1024)
        size = round(size,3)
        return (Resolution,raw_size,size,fps,bitrate,Audio_Type,Frequency,Channels)

def import_vids():
    mypath = ('D:\\Youtube1')
    conn = sqlite3.connect('C:\\Users\\Sambit\\Desktop\\Projects\\Youtube\\Youtube_Scraper\\youtube.db')
    cur = conn.cursor()
    # r=root, d=directories, f = files
    for r, d, f in os.walk(mypath):
        for file in f:
            if file.endswith(("mp4", "mkv", "flv", "wmv", "avi", "mpg", "mpeg")):
                vid_path = os.path.join(r, file)
                vid_id = vid_path[-15:-4]
                vid_type = vid_path[-3:]
                cur.execute("SELECT Video_ID FROM yt_downloaded WHERE Video_ID = ?",(vid_id,))
                if (cur.fetchone()) is None:
                    Resolution,raw_size,size,fps,bitrate,Audio_Type,Frequency,Channels = update_local(vid_path)
                    params = (vid_id,Resolution,raw_size,size,vid_type,fps,bitrate,Audio_Type,Frequency,Channels,0)
                    cur.execute("INSERT OR REPLACE INTO yt_downloaded VALUES (?,?,?,?,?,?,?,?,?,?,?)",params)

    conn.commit()
    conn.close()

def update_vids():
    def is_in_main():
        conn = sqlite3.connect('C:\\Users\\Sambit\\Desktop\\Projects\\Youtube\\Youtube_Scraper\\youtube.db')              
        cur = conn.cursor()
        cur.execute("UPDATE yt_downloaded SET Is_In_Main = 1 WHERE Video_ID IN (SELECT Video_ID FROM yt_downloaded \
                    WHERE Video_ID IN (SELECT Video_ID FROM tb_videos))")
        conn.commit()                                               
        conn.close()
    is_in_main()
    for i in range(2000):
        conn = sqlite3.connect('C:\\Users\\Sambit\\Desktop\\Projects\\Youtube\\Youtube_Scraper\\youtube.db')              
        cur = conn.cursor() 
        cur.execute("SELECT Count(*) FROM yt_downloaded")
        tot = cur.fetchone()
        cur.execute("SELECT Video_ID FROM yt_downloaded WHERE Is_In_Main = 0 LIMIT 50")
        temp = cur.fetchall()
        if len(temp) < 1:
            print("All Videos (locally downloaded) are now in main table tb_videos")
            break
        result = []
        for item in temp:
            cur.execute("UPDATE yt_downloaded SET Is_In_Main = 1 WHERE Video_ID = ?",(item[0],))
            result.append(item[0])
        
        conn.commit()                                               
        conn.close()

        print('Parsing Downloaded Videos :',(i*50),' / ',tot[0],end="\r")
        print(' ')
        youtube_instance = api_key()
        youtube_instance.get_api_key()
        youtube = youtube_instance.get_youtube()
        get_videos_stats(youtube,result,1)
        conn = sqlite3.connect('youtube.db')              
        cur = conn.cursor()
        for item in result:
            print('New Item added successfully :',item)
            cur.execute("UPDATE tb_videos SET Is_Downloaded = 1 WHERE Video_ID = ?",(item,))
            cur.execute("UPDATE tb_videos SET Is_Seen = 1 WHERE Video_ID = ?",(item,))
            cur.execute("UPDATE tb_videos SET Worth = 1 WHERE Video_ID = ?",(item,))
        conn.commit()                                               
        conn.close()
        is_in_main()

if __name__ == "__main__":
    import_vids()
    update_vids()
