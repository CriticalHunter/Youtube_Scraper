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
This project does the following tasks

1. Creates a database for storing all the data
    1. Database is created using sqlite, which comes with python
    2. Database will be placed in the same folder as the project file, named 'youtube.db'
    3. It will have 4 tables - tb_channel, tb_playlist, tb_videos, video_history
    4. You can use programs like [DB Browser](https://sqlitebrowser.org) , which is lightweight, to view the database.
2. Asks if user wants to scrape an entire channel or just a Youtube playlist or gather stats on Watched History

        
## :computer: Setup Guide
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
Install this library in a [virtualenv](https://virtualenv.pypa.io/en/latest/) using pip. 


#### Mac/Linux

```
pip install virtualenv
virtualenv <your-env>
source <your-env>/bin/activate
<your-env> pip install -r requirements.txt
```

#### Windows

```
pip install virtualenv
virtualenv <your-env>
<your-env>\Scripts\activate
<your-env> pip install -r requirements.txt
```


## Working Guide

Run the program YT_Scrape.py

The script will ask for required data in the command line and is pretty self-explanatory (Once it runs)

Else, look the [step-by-step Guide](https://github.com/CriticalHunter/Youtube_Scraper/blob/master/Step-By-Step.md)


## :hearts: Contributing
There are several ways to help. 

1. **Spread the word:** More users means more possible people testing and contributing to the app which in turn means better stability and possibly more and better features. You can [![Twitter](https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Fgithub.com%2FCriticalHunter%2FYoutube_Scraper.git)](https://twitter.com/intent/tweet?text=Wow:&url=https%3A%2F%2Fgithub.com%2FCriticalHunter%2FYoutube_stats.git) or share it on [LinkedIn](http://www.linkedin.com/shareArticle?mini=true&url=https://github.com/CriticalHunter/Youtube_Scraper.git). Every little bit helps ! 

2. **[Make a feature or improvement request](https://github.com/CriticalHunter/Youtube_Scraper/issues/new)**: Something can be be done better? Something essential missing? Let us know! 

3. **[Report bugs](https://github.com/CriticalHunter/Youtube_Scraper/issues/new)**

4. **Contribute**: You don't have to be programmer to help. 
     1. **Treat Me A Coffee Instead** [Paypal](https://paypal.me/CriticalHunter23)


### Pull Requests 
**Pull requests** are of course very welcome! Please make sure to also include the issue number in your commit message, if you're fixing a particular issue (e.g.: `feat: add nice feature with the number #31`).
