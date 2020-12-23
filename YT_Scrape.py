from __future__ import print_function, unicode_literals
import re
import six
import os

from pyfiglet import Figlet
from pprint import pprint
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError
from pyfiglet import figlet_format

from termcolor import colored
import argparse

from src_code import entire_channel, just_playlist, get_channel_details, get_api_key, create_new, load_history, get_playlist_videos





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
log1("Welcome to Email CLI", "green")

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

questions = [
    {
        'type': 'confirm',
        'name': 'Database',
        'message': 'Do you want to create a new database (No, if you already have one)',
        'default': False
    },
    {
        'type': 'input',
        'name': 'key',
        'message': 'Please enter your Youtube API key ',
    },
    {
        'type': 'list',
        'name': 'operation',
        'message': 'What do you want to do?',
        'choices': ['Find oldest videos on a topic', 'Scrape a Channel','scrape a single playlist' ,'Load Your History'],
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
]
answers = prompt(questions, style=style)

if answers['Database'] == True:
    create_new()

get_api_key(answers['key'])

if answers['operation'] == 'find oldest videos on a topic':
    os.system("python oldest_videos.py -h")

elif answers['operation'] == 'scrape a channel':
    if answers['Channel'] == 'Just Channel Stats (Individual video stats are not scraped)':
        get_channel_details(answers['channelID'])
    elif answers['Channel'] == 'Scrape Everything for a channel':
        entire_channel(answers['channelID'])

elif answers['operation'] == 'scrape a single playlist':
    get_playlist_videos(answers['playlistID'])

elif answers['operation'] == 'load your history':
    load_history()

