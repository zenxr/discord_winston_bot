# Winston Bot
A bot that:
* Uses Wolfram Alpha's API to answer questions (more than just math!)
* Picks a random OverWatch hero given hero type
* Returns information about users and roles in a discord server
* Contains a blacklist feature to manage who can interact with the bot
![Alt text](winston.png?raw=true "Optional Title")
### Before Installing
Obtain a wolframalpha API application ID and Discord Application secret token.
### Prerequisites
You must install:
* Python3+ (3.5 used)
* discord.py library
* wolframalpha python library
### Installing and Running
Place the WA app_id and discord app's secret token accordingly in the main bot file (scrappy.py). If you'd like to use just the WA query functionality, it can be found in testingWA.py (place your WA app_id in it first)
* Go into the directory that contains the programs
```
cd ~/Winston
```
* Execute scrappy.py to run the main bot
```
python3.5 scrappy.py
```
* If you'd like to run the files created testing the blacklist and WolframAlpha functions, then:
```
python3.5 testingWA.py
python3.5 testing_blacklist.py
```
### Author
**Cody Stephenson**
