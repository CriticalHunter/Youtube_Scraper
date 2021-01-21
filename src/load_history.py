from datetime import datetime, timedelta
import sqlite3, time
from bs4 import BeautifulSoup

from src.get_video_stats import get_videos_stats
from src.get_api_key import api_key


def update_title():
    conn = sqlite3.connect('youtube.db')              
    cur = conn.cursor()
    cur.execute("SELECT Video_ID FROM video_history WHERE (Title IS NULL OR Title = '') AND Is_Deleted = 0")
    temp = cur.fetchall()
    for item in temp:
        cur.execute("SELECT Video_title FROM tb_videos WHERE Video_ID = ?",(item[0],))
        tit = cur.fetchone()
        cur.execute("UPDATE video_history SET Title = ? WHERE Video_ID = ?",(tit[0],item[0]))
    conn.commit()
    conn.close()
def update_is_seen():
    conn = sqlite3.connect('youtube.db')              
    cur = conn.cursor()
    cur.execute("UPDATE tb_videos SET Is_Seen = 1 WHERE Video_ID IN (SELECT Video_ID FROM tb_videos \
                WHERE Video_ID IN (SELECT Video_ID FROM video_history))")
    conn.commit()                                               
    conn.close()

def update_is_in_main():
    conn = sqlite3.connect('youtube.db')              
    cur = conn.cursor()
    cur.execute("UPDATE video_history SET Is_in_Main = 1 WHERE Video_ID IN (SELECT Video_ID FROM video_history \
                WHERE Video_ID IN (SELECT Video_ID FROM tb_videos))")
    cur.execute("UPDATE video_history SET Is_Deleted = 1 WHERE Video_ID NOT IN (SELECT Video_ID FROM video_history WHERE Video_ID IN (SELECT Video_ID FROM tb_videos))")

    conn.commit()                                               
    conn.close()

def update_history(youtube):
    for i in range(2000):
        conn = sqlite3.connect('youtube.db')              
        cur = conn.cursor() 
        cur.execute("SELECT Count(*) FROM video_history")
        tot = cur.fetchone()
        cur.execute("SELECT Video_ID FROM video_history WHERE Is_in_Main = 0 AND Is_Deleted = 0 LIMIT 50;")
        temp = cur.fetchall()
        if len(temp) < 2:
            print("All Videos From Watched History are now in main table tb_videos")
            break
        result = []
        for item in temp:
            cur.execute("UPDATE video_history SET Is_in_Main = 1 WHERE Video_ID = ?",(item[0],))
            result.append(item[0])
        
        conn.commit()                                               
        conn.close()
        print('Parsing Watch History Videos :',(i*50),' / ',tot[0],end="\r")
        get_videos_stats(youtube,result,1)
        update_is_in_main()

def load_history(res='n'):
    count_loc_prog = 0
    with open("takeout/history/watch-history.html",encoding='utf-8') as fp:
        conn = sqlite3.connect('youtube.db')              
        cur = conn.cursor()

        soup = BeautifulSoup(fp,'lxml')
        soup = soup.body

        videos = soup.find_all("div", {"class": "content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1"})

        print(len(videos))
        
        for video in videos:
            count_loc_prog += 1
            if count_loc_prog % 500 == 0:
                print('Loading into Database : ',count_loc_prog,' / ',len(videos),end="\r")
            tags = video.find_all('a')
            # try:

            if tags == []:
                continue
            
            V_link = tags[0].get('href')
            V_link = V_link.split('=')[-1]
            br_tags = video.find_all('br')
            for tag in br_tags:
                watched_at = str(tag.next_sibling)
                if watched_at[-3:-1] == 'IS':
                    final_time = (watched_at)
                    temp = final_time.replace('IST','+0530')
                    epoch = time.mktime(time.strptime(temp, "%b %d, %Y, %I:%M:%S %p %z"))
            cur.execute("INSERT OR IGNORE INTO video_history VALUES (?,?,?,?,?,?)", (V_link,'',final_time,epoch,0,0))
            

        conn.commit()                                               # Push the data into database
        conn.close()
    print("\n Loaded \n")

    if res == 'y' or res == "Y":
        youtube_instance = api_key()
        youtube_instance.get_api_key()
        youtube = youtube_instance.get_youtube()
        update_history(youtube)
        update_title()
    update_is_seen()
    update_is_in_main()

if __name__ == "__main__":
    pass