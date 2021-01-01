# Youtube_scrape
<img src="https://github.com/CriticalHunter/Youtube_Scraper/blob/master/Assets/title.jpg" >
<p align="center" style="text-align: center;">
<a href="https://lbesson.mit-license.org">
  <img alt="MIT license"
       src="https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square"
       align="center">
<a href="https://twitter.com/intent/tweet?text=Wow:&url=https%3A%2F%2Fgithub.com%2FCriticalHunter%2FYoutube_stats.git"><img alt="Twitter" src="https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Fgithub.com%2FCriticalHunter%2FYoutube_Scraper.git"></a>
    
Scrape data about an entire Channel or just a Playlist, using Youtube API. No OAuth is required.

## :heavy_check_mark: Features
Following features are available :

![CLI](/Assets/example_0.0.jpg)

1. **create_new** : 
     1. It creates a sqlite database to store all data.
     2. Database will be placed in the same folder as the project file, named 'youtube.db'
     3. It will have 4 tables - tb_channel, tb_playlist, tb_videos, video_history
     4. You can use programs like [DB Browser](https://sqlitebrowser.org) , which is lightweight, to view the database.
2. **Oldest Video on A Topic** :
     1. It is an isolate program, that can be run independently.
     2. It doesn't depend on main code or any database.
3. **Scrape A Channel**:
     1. Allows to scrape Channel Details and it's playlists.
     2. It can also scrape details for each video of that channel.
          1. If this option is not chosen, the playlist table won't have Playlist Duration.
4. **Scrape A Single Playlist**:
     1. Allows to scrape info about a single Playlist and details about all it's videos.
5. **Load Your History**:
     1. Make sure you have downloaded google Takeouts for your account to the PWD.
     2. Make sure you have follwing path './takeout/history/watch-history.html'
     3. Option to keep videos of your history on a separate table or integrate them with main table tb_videos
          1. In order to use next features, you have to integrate them.
6. **Most Watched Video**:
     1. You can list your most watched 'n' videos
7. **Early Viewed**:
     1. You can list 'n' videos, which you saw earliest after they were uploaded.
     2. There are some discrepencies, as many videos are reuploaded after you have seen it.
          1. Program ignores those
     3. It now only works when you watched it in IST.
8. **Generate Download List**:
     1. This will create a text file, that will list Youtube URLs that can be downloaded by Youtube-DL or IDM etc.
     2. It will select videos which are marked 'Worth = 1' i the database.
          1. This operation is to be done by the user directly on the database (using DB Browser or such)
     3. There is option to list videos of a single Channel or from entire DAtabase.
     4. *Caution* : Once a video is processed by this function, it will be marked 'Is_Downloaded = 1'. Next time this function is run, new video IDs will be considered.
          1. Hence User must make sure, all videos in *download_list.txt* are downloaded before rewriting the file.

        
## :computer: Setup Guide
Below is a detailed guide on setting up the environment.

### Youtube API
First you need to have you Youtube API key. Below is a link of a video, that will guide you. **Watch from 0:00 - 5:30**
[![Getting Youtube API Key](https://img.youtube.com/vi/th5_9woFJmk/0.jpg)](https://www.youtube.com/watch?v=th5_9woFJmk)
1. **Note - Youtube API is rate limited to 10000 hits/day.**
2. You can view your quotas at [here - console](https://console.cloud.google.com/iam-admin/quotas)
3. Cost of operations is decribed [here -Youtube API docs](https://developers.google.com/youtube/v3/docs)
4. Code has been optimized to decrease quota usage. You can easily work with 50000 videos/day. For more please check your quota limit.

### Installation
You need to install google-api-python-client to run this project. [github API link](https://github.com/googleapis/google-api-python-client)
Install this library in a [virtualenv](https://virtualenv.pypa.io/en/latest/) using pip. 


#### Mac/Linux

```
pip install virtualenv
virtualenv venv
venv/bin/activate
venv pip install -r requirements.txt
```

#### Windows

```
pip install virtualenv
virtualenv venv
venv\Scripts\activate
venv pip install -r requirements.txt
```


## Working Guide

1. Get Your Youtube API key as shown in above video.
2. Pip install the requirements.txt
3. Run the program YT_Scrape.py


The script will ask for required data in the command line and is pretty self-explanatory (Once it runs)

[View Samples](/Samples.md)


## :hearts: Contributing
There are several ways to help. 

1. **Spread the word:** More users means more possible people testing and contributing to the app which in turn means better stability and possibly more and better features. You can [![Twitter](https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Fgithub.com%2FCriticalHunter%2FYoutube_Scraper.git)](https://twitter.com/intent/tweet?text=Wow:&url=https%3A%2F%2Fgithub.com%2FCriticalHunter%2FYoutube_stats.git) or share it on [LinkedIn](http://www.linkedin.com/shareArticle?mini=true&url=https://github.com/CriticalHunter/Youtube_Scraper.git). Every little bit helps ! 

2. **[Make a feature or improvement request](https://github.com/CriticalHunter/Youtube_Scraper/issues/new)**: Something can be be done better? Something essential missing? Let us know! 

3. **[Report bugs](https://github.com/CriticalHunter/Youtube_Scraper/issues/new)**

4. **Contribute**: You don't have to be programmer to help. 
     1. **Treat Me A Coffee Instead** [Paypal](https://paypal.me/CriticalHunter23)


### Pull Requests 
**Pull requests** are of course very welcome! Please make sure to also include the issue number in your commit message, if you're fixing a particular issue (e.g.: `feat: add nice feature with the number #31`).
