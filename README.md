SlackBot

Game Ideas:

Reversi: https://en.wikipedia.org/wiki/Reversi

	Concept: Two human players can play the above game through use of Slackbot.



Users and Use Cases
Define the different types of people that are using.
Define different use cases.

Users: Initially two human players. Possibly expand to human vs AI or AI vs AI.
Use cases: See above ^^^^^^


Technical Requirements
Front-end - not necessary
Back-end - Python/Flask
DB - RethinkDB / MongoDB
Data Format - JSON


Features
Document everything
What is the feature?
How are you going to build it? Technology wise?
How long is it going to take? Two weeks

Features:

Display: ASCII or Image
ASCII easier: Grid marked by [ ], blank implies free space, X implies black, O implies white, available moves marked by +.
Image: Much harder. Have something that demonstrates an image based on the board condition.

How to build image: For ascii, just iterate through double array that is the state of the game! in double array, -1 -> white, 0 -> not taken, 1 -> black. Just convert to a properly formatted string. Other option: make something that encapsulates the state of the board, and have an appropriate toString method.

User interaction!: through slackbot.
While game is being played through slackbot, user can use a keyword that indicates he/she is making a move, along with the grid coordinates of where the move is being attempted. Based on state array, it is easy to check whether a move is available or not. The game will end when one player is unable to make a move!
Ranking!: Like chess!
Maybe a leaderboard as well!!!! Have a database that keeps track of each user’s stats.
Random feature
Any random movement


Minimum Viable Product
A reversi game between two players through slackbot!!!


Timeline
Dates
Milestones
Assigning people to tasks

Week 1
Get set up with Github - @Brian, 1 hour
Create a Hello World Flask app - @Brian, @Bob, 1 hour
Week 2








