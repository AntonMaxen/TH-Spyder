<center><h1>TH-Spyder</h1></center>
<!-- TABLE OF CONTENTS -->

<!--ts-->
## Table of Contents ##
* [Background](#background)
* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
<!--te-->

## Background ##

It all started with a prototype i made to automate the task of checking if my current course have updated a new lecture, so i built a script with BeautifulSoup, Requests and
the discord api wrapper discord.py. It was short and did what i wanted, but it ended at that. If i wanted to scrape another website i had to make another entire program almost, so out came the idea to make one program for all kind of scraping, quick, easy and accessible is what i had in mind. The name TH is coming for the fact that the idea of this project came from the fact that i scraped my schools webplatform where the TH is the name of the school.
<!-- ABOUT THE PROJECT -->
## About The Project
TH-spyder is a model based webscraper with github integration to discords web api. It scrapes a website according to a userdefined model and posts it using a discord webhook, to wanted discord-server. in the model the runtime schedule is also defined using a cron defined schedule. The user can add as many "spiders" as the user want.

### Built With
This section should list any major frameworks that you built your project using. Leave any add-ons/plugins for the acknowledgements section. Here are a few examples.
* [Beautifulsoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [Requests](https://requests.readthedocs.io/en/master/)
* [APScheduler](https://apscheduler.readthedocs.io/)


<!-- GETTING STARTED -->
## Getting Started

Follow the [installation](#installation) to get started

### Prerequisites

* Python 3+

### Installation

1. Clone the repo
```sh
git clone https://github.com/AntonMaxen/TH-Spyder.git
```
2. Install requirements
```sh
pip install requirements.txt 
```
4. Create your scraping model at `thspyder/models/models.json`
```
See model_template.json
```

<!-- USAGE EXAMPLES -->
## Usage

Work in progress

## Components
<img src="https://github.com/AntonMaxen/TH-Spyder/blob/master/uml.png">
