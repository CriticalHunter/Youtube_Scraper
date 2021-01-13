from __future__ import print_function, unicode_literals
import re
import six
import os
import sys

from pyfiglet import Figlet, figlet_format
from pprint import pprint
from PyInquirer import style_from_dict, Token, prompt, Validator, ValidationError
from termcolor import colored
import argparse

from src_code import  load_history, get_playlist_videos, most_watched, early_views, download_n

from src.create_new import create_new
from src.get_api_key import api_key
from src.get_channel_details import get_channel_details
from src.entire_channel import entire_channel



def log1(string, color, figlet=False):
    if colored:
        if not figlet:
            six.print_(colored(string, color))
        else:
            six.print_(colored(figlet_format(
                string, font='doom'), color))
    else:
        six.print_(string)

log1("Youtube_Scraper", color="blue", figlet=True)
log1("Welcome to Youtube_Scraper", "green")

style = style_from_dict({
    Token.QuestionMark: '#E91E63 bold',
    Token.Selected: '#673AB7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#2196f3 bold',
    Token.Question: '',
})



class NumberValidator(Validator):
    def validate(self, document):
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(
                message='Please enter a number',
                cursor_position=len(document.text))  # Move cursor to end


print('Please Choose the desired Options')
print('Press "ctrl+C" to escape at any point\n')

create_new()

if not os.path.exists("key.txt"):
    questions = [
    {
        'type': 'input',
        'name': 'API',
        'message': '"key.txt" file not found. Please enter your Youtube API key '
    },]
    answers = prompt(questions, style=style)
    with open ('key.txt','w') as f:
        f.write(answers['API'])
youtube_instance = api_key()
youtube_instance.get_api_key()
youtube = youtube_instance.get_youtube()
if youtube == None:
    sys.exit()
try:
    questions = [
        {
            'type': 'list',
            'name': 'operation',
            'message': 'What do you want to do?',
            'choices': ['Find oldest videos on a topic', 'Scrape a Channel','Scrape a Single Playlist' ,'Load Your History','Most Watched Video','Early Viewed Video','Generate Download List'],
            'filter': lambda val: val.lower()
        },
        {
            'type': 'list',
            'name': 'Channel',
            'message': 'Select Further \n Scraping all videos for a big channel will surpass your free API Limit',
            'choices': ['Scrape Everything for a channel', 'Just Channel Stats (Individual video stats are not scraped)'],
            'when': lambda answers: answers['operation'] == 'scrape a channel'
        },
        {
            'type': 'input',
            'name': 'channelID',
            'message': 'Enter the Channel ID',
            'when': lambda answers: answers['operation'] == 'scrape a channel' and answers['Channel'] != ''
        },
        {
            'type': 'input',
            'name': 'playlistID',
            'message': 'Enter the Playlist ID',
            'when': lambda answers: answers['operation'] == 'scrape a single playlist'
        },
        {
            'type': 'list',
            'name': 'Download',
            'message': 'What should the list contain?',
            'choices': ['Videos from a single Channel', 'Videos from entire database'],
            'when': lambda answers: answers['operation'] == 'generate download list'
        },
        {
            'type': 'confirm',
            'name': 'import',
            'message': 'Do you want to import your video_history into main table(tb_videos) too? ',
            'default': False,
            'when': lambda answers: answers['operation'] == 'load your history'
        },
    ]

    answers = prompt(questions, style=style)


    if answers['operation'] == 'find oldest videos on a topic':
        os.system("python .\src\oldest_videos.py -h")

    elif answers['operation'] == 'scrape a channel':
        if answers['Channel'] == 'Just Channel Stats (Individual video stats are not scraped)':
            get_channel_details(youtube,answers['channelID'])
        elif answers['Channel'] == 'Scrape Everything for a channel':
            entire_channel(youtube,answers['channelID'])

    elif answers['operation'] == 'scrape a single playlist':
        get_playlist_videos(answers['playlistID'])

    elif answers['operation'] == 'load your history':
        if answers['import'] == True:
            res = 'y'
        elif answers['import'] == False:
            res = 'n'
        print("Please Wait ...")
        load_history(res)

    elif answers['operation'] == 'most watched video':
        print("If your watch history is not loaded in database, it will give empty result")
        print("Please enter, How many items to retrieve e.g. 10 for Top 10 \n")
        n = int(input())
        most_watched(n)

    elif answers['operation'] == 'early viewed video':
        print("If your watch history is not loaded in database, it will give empty result")
        print("Please enter, How many items to retrieve e.g. 10 for Top 10 \n")
        n = int(input())
        early_views(n)

    elif answers['Download'] == 'Videos from a single Channel':
        print("It will list videos that are marked 'Is-Good' and is present in your database")
        chc = input("Please enter the channel ID \t")
        print("Please enter, How many items the list will contain \n")
        n = int(input())
        download_n(chc,n)
    elif answers['Download'] == 'Videos from entire database':
        print("It will list videos that are marked 'Is-Good' and is present in your database")
        chc = ''
        print("Please enter, How many items the list will contain \n")
        n = int(input())
        download_n(chc,n)

except Exception as e:
    print(e)