import sqlite3,datetime,calendar



def absolute_dates():
    year_2020 = 1577836800
    conn = sqlite3.connect('youtube.db')              
    cur = conn.cursor()
    cur.execute("SELECT MIN(epoch) from video_history")
    result = cur.fetchone()
    oldest = int(result[0])
    cur.execute("SELECT MAX(epoch) from video_history")
    result = cur.fetchone()
    newest = int(result[0])

    years = [2018,2019,2020,2021]
    months = [x for x in range(1,13)]
    dates = []
    # days = [x for x in range(1,29)]
    # for year in years:
    #     for month in months:
    #         for day in days:
    #             date = (year,month,day)
    #             dates.append(date)
    # for date in dates:
    #     print(date)
    cal = calendar.calendar
    temp = calendar.itermonthdates(2021, 1)
    print(cal)
    conn.close()

def relative_dates():
    conn = sqlite3.connect('youtube.db')              
    cur = conn.cursor()

    # Absolute, Relative

    start = 1568523230
    end = 1609459199
    max_res = 0
    for start in range (1577836800,1578614400,3600):
        end = start + 31622399
        cur.execute("SELECT COUNT(Video_ID) from video_history WHERE epoch > ? AND epoch < ?",(start,end))
        result = cur.fetchone()
        result = int(result[0])
        
        if result > max_res:
            max_res = result
            start_year = start
            end_year = end
        if start % 10000 == 0:
            print(start)
    conn.close()
    start_year = datetime.datetime.utcfromtimestamp(start_year).replace(tzinfo=datetime.timezone.utc)
    end_year = datetime.datetime.utcfromtimestamp(end_year).replace(tzinfo=datetime.timezone.utc)
    print(max_res,start_year,end_year)

relative_dates()


