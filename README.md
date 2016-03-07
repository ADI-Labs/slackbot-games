:game_die: SlackBot :game_die:
====================

## Usage
### Install 
Install the slack client. 

	sudo pip install slackclient

Clone the repo.

	git clone https://github.com/ADI-Labs/slackbot-games

Create a file `token.json` and add `{"token":"YOUR_TOKEN"}`

	cd slackbot-games
	touch token.json creates token.json


Run the bot in your terminal with:
	
	python bot.py
	
Check slack for the bot.

Sucess!
	

### TO-DOS


## SPEC

#### Game Ideas

Reversi: https://en.wikipedia.org/wiki/Reversi

	Concept: Two human players can play the above game through use of Slackbot.


#### Users

Initially human vs. AI. Expand to two human players in a slack channel.


#### Technical Requirements
* **Back-end** - Python/Flask
* **DB** - RethinkDB or MongoDB (TBD)
* **Data** - JSON

### Features

#### Display
ASCII Grid or Image

#### User interaction
through a slackbot

#### Ranking
Like chess! Maybe a leaderboard as well! Have a database that keeps track of each user’s stats.

#### Minimum Viable Product
A reversi game between two players through slackbot!!!

