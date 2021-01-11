import sqlite3

def early_views(n=5):
    conn = sqlite3.connect('youtube.db')              
    cur = conn.cursor()
    cur.execute("SELECT video_history.Video_ID, video_history.epoch -tb_videos.epoch As diff,video_history.epoch,tb_videos.epoch,tb_videos.Video_title,tb_videos.epoch, Watched_at FROM video_history \
                    LEFT OUTER JOIN tb_videos on tb_videos.Video_id = video_history.Video_ID WHERE (diff-19800) > 0 GROUP BY video_history.Video_ID ORDER BY diff ASC ;")
    results = cur.fetchmany(n)
    print("Video ID","      Diff in Min","\t","Published AT(UTC)"," Watched AT (IST)","\tVideo Title")
    print("-------------------------------------------------------------------------------------------------------")
    for result in results:
        Link = result[0]
        differ = (int(result[1])-19800)/60
        differ1 = ("{:6d}".format(int(differ//1)))
        differ2 = ("{:.2f}".format(differ % 1)).replace('0.','.')
        differ = differ1+differ2
        print(Link,'\t',differ,'\t',result[2],'\t',result[3],'\t',result[4])
    conn.commit()                                               
    conn.close()

if __name__ == "__main__":
    pass