# Youtube_stats
Scrape data about an entire Channel or just a Playlist, using Youtube API. No OAuth is required.

## Details
This project does the following tasks

1. Creates a database for storing all the data
    1. Database is created using sqlite, which comes with python
    2. Database will be placed in the same folder as the project file, named 'youtube.db'
    3. It will have 3 tables - tb_channel, tb_playlist, tb_videos
    4. Primary and Foreign keys are there to link the tables
    5. You can use programs like [DB Browser](https://sqlitebrowser.org) , which is lightweight, to view the database.
2. Asks if user wants to scrape an entire channel or just a Youtube playlist
3. Stores relevant data in corresponding tables
    1. For entire channel it will store
        1. Channel details in tb_channels
        2. All playlists created by the channel in tb_playlists 
        3. Videos in those playlist may/may not be uploaded by the channel. (e.g. it may be a playlist of compiled videos of other users)
        4. In that case, videos will have their original data as uploaded by original account
        5. All video data will be stored in tb_videos
    2. For single playlist it will store
        1. Only video data in tb_videos
        
## Setup Guide
Below is a detailed guide on setting up the environment.

### Youtube API
First you need to have you Youtube API key. Below is a link of a video, that will guide you. **Watch from 0:00 - 5:30**
[![Getting Youtube API Key](https://img.youtube.com/vi/th5_9woFJmk/0.jpg)](https://www.youtube.com/watch?v=th5_9woFJmk)
1. **Note - Youtube API is rate limited to 10000 hits/day.**
2. You can view your quotas at [here - console](https://console.cloud.google.com/iam-admin/quotas)
3. Cost of operations is decribed [here -Youtube API docs](https://developers.google.com/youtube/v3/docs)
4. Code has been optimized to decrease quota usage. You can easily work with 5000 videos/day. For more please check your quota limit.

### Installation
You need to install google-api-python-client to run this project. [github API link](https://github.com/googleapis/google-api-python-client)
Install this library in a [virtualenv](https://virtualenv.pypa.io/en/latest/) using pip. virtualenv is a tool to
create isolated Python environments. The basic problem it addresses is one of
dependencies and versions, and indirectly permissions.

With virtualenv, it's possible to install this library without needing system
install permissions, and without clashing with the installed system
dependencies.

#### Mac/Linux

```
pip install virtualenv
virtualenv <your-env>
source <your-env>/bin/activate
<your-env>/bin/pip install google-api-python-client
```

#### Windows

```
pip install virtualenv
virtualenv <your-env>
<your-env>\Scripts\activate
<your-env>\Scripts\pip.exe install google-api-python-client
```
## Working Guide

Run the program YT_data.py

The script will ask for required data in the command line and is pretty self-explanatory (Once it runs)

### Case 1 - Scraping Entire Channel, when Channel ID is known

![example_1.1](/Assets/example_1.1.jpg)
![example_1.2](/Assets/example_1.2.jpg) ![example_1.3](/Assets/example_1.3.jpg)
![example_1.4](/Assets/example_1.4.jpg) ![example_1.5](/Assets/example_1.5.jpg)
![example_1.6](/Assets/example_1.6.jpg) ![example_1.7](/Assets/example_1.7.jpg)

### Case 2 - Scraping Entire Channel, when Channel name is known (ID is preferable-Case 1)

![example_1.1](/Assets/example_1.1.2.jpg)
![example_1.2](/Assets/example_1.5.2.jpg) ![example_1.3](/Assets/example_1.5.3.jpg)

### Case 3 - Scraping a single Playlist

![example_1.1](/Assets/example_2.1.jpg)
![example_1.2](/Assets/example_2.2.jpg)

## Database (in DB Browser) sample results
### Database Schema
![example_0.1](/Assets/example_0.1.jpg)
### tb_channels Table
![example_0.2](/Assets/example_0.2.jpg)
### tb_playlists Table
![example_0.3](/Assets/example_0.3.jpg)
### tb_videos Table
![example_0.4](/Assets/example_0.4.jpg)

![example_0.5](/Assets/example_0.5.jpg)


