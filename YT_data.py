from src_code import entire_channel, just_playlist, get_channel_id, get_api_key
from sqlite_create import create_new

while True:
    print("Do you want to create a new Database?")
    response = input("Enter  (Y/N) ")
    if response == 'Y' or response == 'y':
        create_new()
        break
    elif response == 'N' or response == 'n':
        print("\n If database is not there, it will cause error.\n\n")
        break
    else:
        print("\n Print enter a valid response (Y/N) \n")

print("Please enter your Youtube API key ")
key = input()
get_api_key(key)


print("Do you want to scrape a channel or just a playlist? (Enter 1 for channel, 2 for playlist)")
choice = input("Enter either '1' or '2' \n")

if choice == '1':
    print("\n\nProceed with channel ID or Name, (Enter 1 for ID, 2 for name) ")
    selection = input("Enter either '1' or '2' \n")
    while True:
        if selection == '1':
            print("\nPlease get the channel ID, then enter below (E.g. mkojWltnsuoSku-abcdhfIw")
            ch_id = input("Please enter the channel id -  ")
            break
        elif selection == '2':
            print("\nPlease get the channel Name, then enter below (E.g. pewdiepie)")
            ch_name = input("Please enter the channel Name -  ")
            ch_id = get_channel_id(ch_name)
            print('\n Check the subscriber count and decide if the program detects the correct channel')
            k = input('please enter (Y/N)')
            if k == 'y' or k == 'Y':
                break
            else:
                print("Please enter a valid ID or name")

    entire_channel(ch_id)
elif choice == '2':
    print("PLease Enter the Playlist ID (comes after playlist?list=)")
    playlist_id = input("playlist?list= ")
    just_playlist(playlist_id)
else:
    print("Please enter a valid choice next time")