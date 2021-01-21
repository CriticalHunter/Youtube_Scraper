import pprint
from bs4 import BeautifulSoup
import re
import sqlite3
import time
import datetime,pytz

with open("test.html",encoding='utf-8') as fp:                                      # To open a local html file
    soup = BeautifulSoup(fp,features='lxml')

soup_str = soup.prettify()                                            # Prettify the HTML, but it becomes String
with open('temp.html','w',encoding='utf-8') as wr:
    wr.write(soup_str)

tags = soup.find_all("c-wiz", {"class": "xDtZAf"})
for tag in tags:
    with open("watched.txt",'a',encoding='utf-8') as f:
        date = tag.get('data-date')
        foo = tag.find("div", {"class": "QTGV3c"})
        temp = (foo.get_text())
        watched = temp.split(' ')
        watched = watched[0]
        if watched == 'Watched':
            try:
                bar = foo.a.get('href')
                vid_id = bar[-11:]
                time = tag.find("div", {"class": "H3Q9vf XTnvW"})
                time = time.get_text()
                f.write(date)
                f.write(' ')
                tm = re.findall('\d+:\d+ .M',time)[0]
                tm1=tm.split(':')[0]
                tm2=tm.split(':')[1]
                tm21 = tm2.split(' ')[0]
                tm22 = tm2.split(' ')[1]
                if len(tm1)==1:
                    tm='0'+tm1+':'+tm21+':'+'00'+' '+tm22
                else:
                    tm=tm1+':'+tm21+':'+'00'+' '+tm22
                f.write(tm)
                f.write(' ')
                f.write(vid_id)
                f.write('\n')
            except:
                pass

with open("watched.txt",'r',encoding='utf-8') as fhand:
    conn = sqlite3.connect('youtube.db')              
    cur = conn.cursor()
    for line in fhand:
        time = line[0:-12]
        p='%Y%m%d %I:%M:%S %p '
        epoch = (datetime.datetime.strptime(time, p))
        # dtobj3=dtobj1.replace(tzinfo=pytz.UTC) #replace method
        # dtobj_kolkata=dtobj3.astimezone(pytz.timezone("Asia/Kolkata"))
        # epoch = dtobj_kolkata.timestamp()
        new_format = epoch.strftime('%b %d, %Y, %I:%M:%S %p')
        vid_id = line[-12:-1]
        cur.execute("INSERT OR IGNORE INTO video_history VALUES (?,?,?,?)", (vid_id,new_format,epoch.timestamp(),0))
    conn.commit()
    conn.close()
