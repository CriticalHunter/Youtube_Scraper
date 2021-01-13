from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from httplib2 import ServerNotFoundError
from google.auth.exceptions import DefaultCredentialsError
'''
Get the API key and save it in a text file named, key.txt in parent folder.
The method to get a youtube API key is well illustrated in the Youtube Video in the README page.
'''
class api_key():
    def __init__(self):
        self.youtube = None

    def get_api_key(self):
        try:
            with open('key.txt') as key_file: 
                api_key = key_file.read()
                youtube = build('youtube','v3',developerKey=api_key)
                self.youtube = youtube

        except HttpError:
            print("\nAPI Key is wrong")
            print("Please recheck the API key or generate a new key.\nThen modify the 'key.txt' file with new Key\n")

        except ServerNotFoundError:
            print("\nUnable to connect to internet...")
            print("Please Check Your Internet Connection.\n")

        except DefaultCredentialsError:
            print("\n'key.txt' is Blank.")
            print("Please save your API key there and then continue.\n")
        
        except FileNotFoundError:
            print("\nNo such file: 'key.txt'")
            print("Please create a file named 'key.txt' and place your Youtube API key in it.\n")

        except Exception as e:
            print(e)
            print("Oops!", e.__class__, "occurred.")

    def get_youtube(self):
        return self.youtube

if __name__ == "__main__":
    youtube_instance = api_key()
    youtube_instance.get_api_key()
    youtube = youtube_instance.get_youtube()    
    print(youtube)