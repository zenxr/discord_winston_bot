# look up a player
import requests
import json
from discord.message import Message


def playerLookup(playerID, mode):
    # have to customize user agent
    head = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'
    }
    # open the url
    url = "https://owapi.net/api/v3/u/"
    # configure parameters (will be changed later)
    user = 'Poseidon-12214'
    category = 'heroes'
    gameType = mode
    # make the request and convert the json to dictionary
    r = requests.get(url + playerID + "/" + category, headers=head)
    data = r.json()
    # get play_time data
    playTime = data["us"]["heroes"]["playtime"][gameType]
    # remove all heroes with 0 hours
    cleanPT = {hero : time for hero,time in playTime.items() if time}
    # convert playtime to minutes
    for key in cleanPT:
        cleanPT[key] = int(cleanPT[key] * 60)
    # sort into a decreasing list of tuples
    sortedPT = sorted(cleanPT.items(), key=operator.itemgetter(1))
    sortedPT.reverse()
    # we now have a list of heroes and playtimes sorted by most played in a list of tuples
    stats = data["us"]["heroes"]["stats"][gameType]
    # we only want to include the 5 heroes with most playtime
    count = 0
    outputHeroData = {}
    for hero in sortedPT:
        if count == 6:
            break
        count = count + 1
        games_played = stats[hero[0]]["general_stats"]["games_played"]
        if (stats[hero[0]]["general_stats"]["games_lost"] == games_played):
            games_won = 0
        else:
            games_won = stats[hero[0]]["general_stats"]["games_won"]
        if games_played == 0:
            winRate = 0
        else:
            winRate = games_won/games_played
        outputHeroData[hero[0]] = [hero[1], winRate]
    outputHeroData_sorted = sorted(outputHeroData.items(), key=lambda x:x[1])
    outputHeroData_sorted.reverse()
    return(outputHeroData_sorted)

# function to split strings into lists of single words
def splitmessage(s):
    words = []
    inword = 0
    for c in s:
        if c in " \r\n\t": #whitepsace
            inword = 0
        elif not inword:
            words = words + [c]
            inword = 1
        else:
            words[-1] = words[-1] + c
    return words

# if player lookup
def player(message):
        elif m[1] == "player":
            mode = "competitive"
            # future functionality, if checking quickplay stuff edit ehre
            #if len(m) == 4:
            #    mode = m[3]
            playerstats = playerLookup(m[2], mode)
            outputMsg = "\r\n```diff\r\n"
            outputMsg = outputMsg + "Stats for " + m[2] + "\r\n\r\n"
            outputMsg = outputMsg + "---------------------------------------------------\r\n"
            outputMsg = outputMsg + "|  Hero Name     |     Time Played |      WinRate |\r\n"
            outputMsg = outputMsg + "---------------------------------------------------"
            for hero in playerstats:
                outputHeroString = "  " + hero[0]
                while len(outputHeroString) < 16:
                    outputHeroString = outputHeroString + " "
                outputMsg = outputMsg + "\r\n|" + outputHeroString + "|"
                if (hero[1][0] // 60) == 0:
                    outputHeroTime = str(hero[1][0] % 60) + "mins |"
                else:
                    outputHeroTime = str(hero[1][0] // 60) + " hr, " + str(hero[1][0] % 60) + " mins |"
                while len(outputHeroTime) < 18:
                    outputHeroTime = " " + outputHeroTime
                outputMsg = outputMsg + outputHeroTime
                outputHeroWinRate = str(int(hero[1][1]*100)) + "% winrate |"
                while len(outputHeroWinRate) < 15:
                    outputHeroWinRate = " " + outputHeroWinRate
                outputMsg = outputMsg + outputHeroWinRate
            outputMsg = outputMsg + "```"
            await client.send_message(message.channel, outputMsg)