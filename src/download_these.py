import sqlite3

def download_n(chc='',n=50):
    with open("download_list.txt",'w',encoding='utf-8') as fp:
        conn = sqlite3.connect('youtube.db')              
        cur = conn.cursor()
        if chc == '':
            cur.execute("SELECT Video_ID FROM tb_videos WHERE Worth = 1 and Is_Downloaded = 0 LIMIT ?",(n,))
        else:
            try:
                cur.execute("SELECT Video_ID FROM tb_videos WHERE Worth = 1 and Is_Downloaded = 0 and Channel_ID = ? LIMIT ?",(chc,n))
            except:
                print("Please enter correct Channel ID")
        down_list = cur.fetchall()
        for item in down_list:
            link = "https://www.youtube.com/watch?v="+item[0]
            cur.execute("UPDATE tb_videos SET Is_Downloaded = 1 WHERE Video_ID = ?",(item[0],))
            fp.write(link)
            fp.write('\n')
        conn.commit()                                               # Push the data into database
        conn.close()

if __name__ == "__main__":
    pass