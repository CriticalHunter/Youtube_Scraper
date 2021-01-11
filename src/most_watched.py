import sqlite3

def most_watched(n=5):
    conn = sqlite3.connect('youtube.db')              
    cur = conn.cursor()
    cur.execute("SELECT video_history.Video_ID,COUNT(video_history.Video_ID) AS cnt, Video_title FROM video_history \
                    LEFT OUTER JOIN tb_videos on tb_videos.Video_ID = video_history.Video_ID \
                    GROUP BY video_history.Video_ID ORDER BY cnt DESC;")
    results = cur.fetchmany(n)
    print("\t","  Video Link","\t","\t","\t","   Times Watched","\t","\t","      Video Name")
    print("-------------------------------------------------------------------------------------------------------")
    for result in results:
        Link = "https://www.youtube.com/watch?v="+result[0]
        if result[2] is None:
            title = "Video is not available in local database"
        else:
            title = result[2]
        print(Link,'\t',result[1],'\t',title)
    conn.commit()                                               
    conn.close()

if __name__ == "__main__":
    pass