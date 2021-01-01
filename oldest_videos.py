from src_code import get_api_key

import argparse
import os
from datetime import datetime

parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,\
                                description='Explore the oldest videos on a Topic',\
                                 epilog='''Examples \n .\oldest_videos.py tesla \n .\oldest_videos.py "game of thrones" -n 15 -s 2012''')
parser.add_argument("topic", help='Enter the topic')
group2 = parser.add_argument_group()
group2.add_argument('-n','--max_results',type=int, metavar='', default=5, help='The script will display "n" results')
group2.add_argument('-s','--start_year',type=int, metavar='', default=2005, help='By default, it will search from 2005')
group2.add_argument('-e','--end_year',type=int, metavar='', default=2010, help='By default, it will search till 2010')

parser.add_argument('-o','--output', action='store_true', help='output to a File')


args = parser.parse_args()


def oldest_videos_on_a_topic(topic,Max_limit,start_yr,end_yr):
    if args.output:
        f = open("old_videos.txt",'w',encoding = 'utf-8')
        f.close()
    else:
        print('\n')
        print('Video ID','\t','Upload Date/Time','\t','Video Title')
        print('--------','\t','----------------','\t','-----------')
    limit = 0
    global youtube
    start_time = datetime(year=2005, month=4, day=1).strftime('%Y-%m-%dT%H:%M:%SZ')
    end_time = datetime(year=2010, month=1, day=1).strftime('%Y-%m-%dT%H:%M:%SZ')

    res = youtube.search().list(part='snippet',
                            q=topic,
                            type='video',
                            publishedAfter=start_time,
                            publishedBefore=end_time,
                            maxResults=50).execute()
    for item in sorted(res['items'], key=lambda x:x['snippet']['publishedAt']):
        title = str(item['snippet']['title']).replace('&#39;',"'").replace('&quot;','"')
        if topic.lower() in title.lower():
            limit += 1
            date_format = "%Y-%m-%dT%H:%M:%SZ" 
            publishedAt = datetime.strptime(item['snippet']['publishedAt'], date_format)
            if args.output:
                f = open("old_videos.txt",'a',encoding = 'utf-8')
                f.write(item['id']['videoId']+'\t\t'+str(publishedAt)+'\t\t'+ title )
                f.write('\n')
                f.close()
            else:
                print(item['id']['videoId'],'\t',publishedAt,'\t', title )
            if limit == Max_limit:
                break
        else:
            continue

    if args.output:   
        print('\nDone! Check the file old_video.txt\n')
    else:
        print('\n')

if __name__ == "__main__":
    key = input("Enter key\n")
    youtube = get_api_key(key)
    oldest_videos_on_a_topic(args.topic,args.max_results,args.start_year,args.end_year)