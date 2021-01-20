
def get_channel_id(youtube,ch_name):
    request = youtube.channels().list(
            part="snippet,contentDetails,statistics",
            forUsername=ch_name
        )
    response = request.execute()
    try:
        sub_count = int(response['items'][0]['statistics']['subscriberCount'])
        if sub_count > 1000000:
            sub_count = str(sub_count / 1000000)
            sub_count = sub_count + 'M Subscribers'
        elif sub_count > 1000:
            sub_count = str(sub_count / 1000)
            sub_count = sub_count + 'K Subscribers'
        else:
            sub_count = str(sub_count) + ' Subscribers'
        ch_id = response['items'][0]['id']
        
        print(" ")
        print(sub_count)
        print(ch_id)
        return ch_id
    except KeyError:
        print(" ")
        print("          Error : Channel not Found ")
        print(" ")

if __name__ == "__main__":
    pass