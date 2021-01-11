from src.get_channel_playlists import get_channel_playlists
from src.get_channel_details import get_channel_details
from src.get_playlist_videos import get_playlist_videos
from src.get_channel_videos import get_channel_videos

def entire_channel(youtube,ch_id):
    get_channel_details(youtube,ch_id)
    playlists_list = get_channel_playlists(youtube,ch_id)
    count = 0
    print('\nThere are ',len(playlists_list),' original/imported playlists\n')
    for playlist in playlists_list:
        count += 1
        print('\nParsing playlist ',count,' \\ ',len(playlists_list))
        get_playlist_videos(youtube,playlist)
    get_channel_videos(youtube,ch_id)