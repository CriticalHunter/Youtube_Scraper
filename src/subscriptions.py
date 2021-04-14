import json

with open("takeout/subscriptions/subscriptions.json", encoding="utf-8") as f:
    subs = json.load(f)
    i = 0
    sub_list = []
    for sub in subs:
        temp = (sub["contentDetails"]["totalItemCount"], sub["snippet"]["resourceId"]["channelId"], sub["snippet"]["title"] )
        # temp = (sub["snippet"]["title"])
        # sub_list.append(temp.title())
        sub_list.append(temp)
    sub_list = list(set(sub_list))
    new_lst = []
    for sub in sub_list:
        temp = sub[2].title()
        sub = (sub[0], sub[1], temp)
        new_lst.append(sub)
    new_lst.sort(key=lambda x:x[2])
    for sub in new_lst:
        print(sub)