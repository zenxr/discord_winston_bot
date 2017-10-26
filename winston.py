import discord
import asyncio
import wolframalpha
import re
import random
import time
import json
import requests
import operator

# create a new client
client = discord.Client()
# secret token
token = 'your_token'
# app_id for wolfram alpha API
app_id = 'your_WA_app_id'

# text-to-speech variable
ttsbool = False 

# my user ID for discord
ownerID = "your_owner_id"

# long concatenated help message
# '```texttexttext```' puts a neat box around the message
helpm = " \r\nI'm Winston.\r\nAsk me anything and I'll try to answer.\r\n"
helpm = helpm + "```Valid commands:\r\n===============\r\n"
helpm = helpm + "!help,\r\n"
helpm = helpm + "!winston playlist show (prints saved playlists), \r\n"
helpm = helpm + "!winston playlist add title url (title = name, url = YT playlist url), \r\n"
helpm = helpm + "!winston playlist remove title (title must be found via playlist show), \r\n"
helpm = helpm + "!winston player (playerID) (gamemode -- optional), \r\n"
helpm = helpm + "!winston pick hero (all|attack|support|tank|defense|team),\r\n"
helpm = helpm + "!role list (list roles on this server), \r\n"
helpm = helpm + "!role (rolename) (print the permissions of a role), \r\n"
helpm = helpm + "!user roles (@username) (list the roles of a specific user),\r\n"
helpm = helpm + "!tts (toggles bot's text-to-speech. Currently : " + str(ttsbool) + "),\r\n"
helpm = helpm + "!clean (cleans bot messages, requires Manage Messages permission),\r\n"
helpm = helpm + "!winston blacklist (add|remove) @user,\r\n"
helpm = helpm + "!winston blacklist print (prints the current blacklisted IDs),\r\n"
helpm = helpm + "!winston (question, math included)```"

# create a wolfram alpha client
clientWA = wolframalpha.Client(app_id)

class Blacklist(object):
    # represents a blacklist
    # functions : add, remove, create, search
    
    def __init__(self, path):
        self.path = path
        f = open(self.path, 'r')
        self.blist = [line.rstrip('\n') for line in f.readlines()]
        f.close()

    def remove(self, account, invokee):
        update = False
        for line in self.blist:
            if account in line:
                self.blist.remove(account)
                update = True
        # if the account was in the list
        if update == True:
            f = open(self.path, 'w')
            for line in self.blist:
                f.write(line + '\n')
            f.close()
            # refresh blist after modification
            f = open(self.path, 'r')
            self.blist = [line.rstrip('\n') for line in f.readlines()]
            f.close()

    def add(self, account, invokee):
        update = True
        for line in self.blist:
            if account in line:
                update = False
        # if the account was not found
        if update == True:
            f = open(self.path, 'a')
            f.write(account + '\n')
            f.close()
            # refresh blist after modification
            f = open(self.path, 'r')
            self.blist = [line.rstrip('\n') for line in f.readlines()]
            f.close()
                    
    def output_list(self, invokee):
        # return all members in the blacklist
        return self.blist
class Playlists(object):
    # represents a list of playlists with IDs
    # functions : add, remove, create, search
    def __init__(self, path):
        self.path = path
        f = open(self.path, 'r')
        self.plists = [line.rstrip('\n') for line in f.readlines()]
        f.close()
    
    def remove(self, user):
        update = False
        for line in self.plists:
            if user in line:
                self.plists.remove(line)
                update = True
        # if the account was in the list, update the file
        if update:
            f = open(self.path, 'w')
            for line in self.plists:
                f.write(line + '\n')
            f.close()
            # refresh plists after modification
            f = open(self.path, 'r')
            self.plists = [line.rstrip('\n') for line in f.readlines()]
            f.close()
    def add(self, user, url):
        update = True
        for line in self.plists:
            if user in line:
                update = False
        # if the user was not found
        if update:
            f = open(self.path, 'a')
            f.write(user + ' ' + url + '\n')
            f.close()
            # refresh plists after modification
            f = open(self.path, 'r')
            self.plists = [line.rstrip('\n') for line in f.readlines()]
            f.close()
    def search(self, user):
        found = "Not found"
        for line in self.plists:
            if user in line:
                chunkedLine = splitmessage(line)
                found = chunkedLine[1]
        return found

    def output_list(self):
        # return the playlists
        return self.plists

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

# checks if a message's author is the bot
def is_me(m):
    return m.author == client.user

# function to randomly select a hero, pass it a string
def pickAHero(category):
    attack = ["Doomfist", "Genji", "McCree", "Pharah", "Reaper", "Soldier76", "Sombra"]
    defense = ["Tracer", "Bastion", "Hanzo", "Junkrat", "Mei", "Torbjorn", "Widowmaker"]
    tank = ["D.Va", "Orisa", "Reinhardt", "Roadhog", "Winston", "Zarya"]
    support = ["Ana", "Lucio", "Mercy", "Symmetra", "Zenyatta"]
    allheros = [attack, defense, tank, support]
    if category == "all":
        # generate random # to pick one of the hero types
        num = random.randint(0, len(allheros)-1)
        # randomly pick one of the heroes from the hero type picked
        return(allheros[num][random.randint(0, len(allheros[num])-1)])
    elif category == "defense":
        # pick one of the members in defense randomly
        return(allheros[1][random.randint(0, len(allheros[1])-1)])
    elif category == "attack":
        return(allheros[0][random.randint(0, len(allheros[0])-1)])
    elif category == "tank":
        return(allheros[2][random.randint(0, len(allheros[2])-1)])
    elif category == "support":
        return(allheros[3][random.randint(0, len(allheros[3])-1)])
    elif category == "team":
        attDef = random.randint(0, 1)
        result = ['', '', '', '', '', '']
        if attDef == 0:
            result[0] = pickAHero("attack")
        else:
            result[0] = pickAHero("defense")
        attDef = random.randint(0, 1)
        if attDef == 0:
            result[1] = pickAHero("attack")
            while result[0] == result[1]:
                result[1] = pickAHero("attack")
        else:
            result[1] = pickAHero("defense")
            while result[0] == result[1]:
                result[1] = pickAHero("defense")
        result[2] = pickAHero("tank")
        result[3] = pickAHero("tank")
        while result[3] == result[2]:
            result[3] = pickAHero("tank")
        result[4] = pickAHero("support")
        result[5] = pickAHero("support")
        while result[5] == result[4]:
            result[5] = pickAHero("tank")
        return(result)
    else:
        # if the function is ran & invalid string, return error
        return("Valid options : defense, attack, tank, support")

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

# this runs when the client initally connects
@client.event
async def on_ready():
    # print info to terminal
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    # print connected servers
    for server in client.servers:
        print(server.name)
    print('------')

# this runs when a member joins a server
# (only once, when they're invited)
@client.event
async def on_member_join(member):
    helpmessage = helpm
    tmp = await client.send_message(member.server, helpmessage)

# this runs when any message is sent in a connected channel
@client.event
async def on_message(message):
    # use the global blacklist instance
    global blacklist
    blacklisted = False
    for name in blacklist.blist:
        if ("<@!" + message.author.id + ">" == name) or ("<@" + message.author.id + ">" == name):
            # blacklisted user, deny access
            blacklisted = True
    if blacklisted and message.author.id != ownerID:
        return
    # !help command
    if message.content.startswith('!help'):
        helpmessage =  message.author.mention + helpm
        await client.send_message(message.channel, helpmessage)
    if message.content.startswith('!clean'):
        deleted = await client.purge_from(message.channel, limit=50, check=is_me)
        await client.send_message(message.channel, 'Deleted {} message(s)'.format(len(deleted)))

    if message.content.startswith('!tts'):
        global ttsbool
        ttsprev = ttsbool
        if ttsbool == True:
            ttsbool = False
        else:
            ttsbool = True
        response = "*Toggling text-to-speech from " + str(ttsprev) + " to " + str(ttsbool) + ".*"
        await client.send_message(message.channel, response)

    if str(message.content) == str(message.content).isupper():
        m = splitmessage(message.content)
        if str(m) == str(m.upper()):
            await client.send_message(message.channel, message.author.mention + "\r\n*chill brah*")
    # !sudoku command
    elif message.content.startswith('!sudoku'):
        await client.send_message(message.channel, "*gg*")
        await client.send_file(message.channel, "seppuku.gif")

    # !genji command
    elif message.content.startswith('!genji'):
        msg = '*MADA MADA*'
        await client.send_message(message.channel, msg, tts=ttsbool)

    # !user, roles command    
    elif message.content.startswith('!user'):
        m = splitmessage(message.content)
        # if message is !user roles @Username, print their roles
        if m[1] == "roles":
            idnum = m[2]
            member = ''
            msg = ''
            # remove <, >, and @ characters (fix issue occuring @everyone)
            for char in idnum:
                if char in "<>@":
                    idnum = idnum.replace(char, '')
            # see if there's a matching member in the message's server
            for memb in message.server.members:
                if idnum in memb.id:
                    member = memb
            # member found
            if member != '':
                msg = "For member " + member.mention + " roles are :\r\n"
                for role in member.roles:
                    msg = msg + '\t' + re.sub('@', '', str(role)) + "\n"
            # member not found
            else:
                msg = "User not found, make sure you @mention them."
            await client.send_message(message.channel, msg)

    # !role command, role list & role rolename        
    elif message.content.startswith('!role'):
        # split message into list
        m = splitmessage(message.content)
        msg = ''
        # if second word is list
        if m[1] == "list":
            msg = '```\r\nThe server roles are : \r\n'
            for role in message.server.roles:
                # remove @ character, fixes @everyone
                msg = msg + '\t' + re.sub('@', '', str(role)) + '\n'
        else:
            # if the specified role exists
            for role in message.server.roles:
                if str(role) == m[1]:
                    msg = ("```For role : " + role.name + "\r\n===================\r\n")
                    msg = msg + ("permisions : \r\n")
                    for perm in role.permissions:
                        if perm[1]:
                            msg = msg + "\t" + str(perm[0] + ",\r\n")
        # if msg is still empty, role not found
        if msg == '':
            msg = "Couldn't find role, invalid input"
        else:
            # finish the pretty box
            msg = msg + '```'
        await client.send_message(message.channel, msg)

    # !pause, currently unfinished
    # function is to have the bot ignore input
    # until owner says resume/unpause
    elif message.content.startswith('!pause'):
        # stop taking input until told to resume
        print("Paused")


    # !winston commands for wolframAlpha queries + special queries
    elif message.content.startswith('!winston'):
        # split message into a list of words
        m = splitmessage(message.content)

        # if message starts with "!winston pick hero"
        if m[1] == "pick" and m[2] == "hero":
            # if message = "!winston pick hero"
            if len(m) == 3:
                hero = pickAHero("all")
                print("Picking hero : " + hero)
            else:
                # pick with the 4th word as the specified subtype of hero
                hero = pickAHero(m[3])
                print("Picking hero (" + m[3] + ") : " + str(hero))
            await client.send_message(message.channel, message.author.mention + ' : ' + str(hero), tts=ttsbool)
        
        # if doing stuff with user playlists
        elif m[1] == "playlist":
            global playlists
            returnMsg = "```"
            if m[2] == "show":
                pl = playlists.output_list()
                for line in pl:
                    returnMsg = returnMsg + line + "\r\n"
                await client.send_message(message.channel, returnMsg + "```")
            elif m[2] == "add":
                playlists.add(m[3], m[4])
                returnMsg = "Added playlist named " + m[3] + " to list"
                await client.send_message(message.channel, returnMsg)
            elif m[2] == "remove":
                playlists.remove(m[3])
                await client.send_message(message.channel, "Removed playlist named : " + m[3])
            else:
                url = playlists.search(m[2])
                if url == "Not found":
                    await client.send_message(message.channel, message.author.mention + ' Sorry! Playlist not found')
                else:
                    await client.send_message(message.channel, message.author.mention + ' : enqueued playlist ' + m[2])
                    await client.send_message(message.channel, "!play " + url)
        # if player lookup
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
        # if blacklist command
        elif m[1] == "blacklist":
            canKick = False
            # issue here?
            #for role in message.author.roles:
            #    if role.permissions.kick_members:
            #        print("Can kick!")
            #        canKick = True

            # make sure we have enough input to work
            if len(m) == 4:
                if m[2] == "add":
                    if (message.author.id == ownerID) or canKick:
                        blacklist.add(m[3], message.author)
                        print("Message.author == " + message.author.id)
                        await client.send_message(message.channel, "User " + m[3] + " has been added to the blacklist.")
                elif (message.author.id == ownerID) and (m[2] == "remove"):
                    for char in m[3]:
                        if char in "<>@":
                            m[3].replace(char, '')
                    blacklist.remove(m[3], message.author)
                    await client.send_message(message.channel, "User " + m[3] + " has been removed from the blacklist.")
            elif m[2] == "print":
                res = "```"
                for line in blacklist.blist:
                    res = res + '\n' + line
                res = res + "```"
                await client.send_message(message.channel, res)
            else:
                # either no name for add or remove or invalid blacklist command
                await client.send_message(message.channel, "Invalid input. Make sure you @mention the user.")

        # !winston hello command, send dank bananas
        elif str(message.content) == "!winston hello":
            await client.send_file(message.channel, "winston.png")
            await client.send_message(message.channel, message.author.mention + '\r\n' + "Hello.", tts=ttsbool)
        # if not a hard-coded command, query WA
        else:
            print("Entering query")
            # remove the first word from message.content
            strippedMessage = message.content.split(' ', 1)[1]
            # query WA, save to res (response)
            res = clientWA.query(strippedMessage)
            # im bad with variable names :D
            bool = 0
            # attempt to understand WA data. If WA doesn't understand the question, except error
            try:
                # WA has python API
                # pods are similar to a list object
                for item in res.pods:
                    streng = ''
                    # if this pod is marked as primary/Result
                    if item.primary or item.title == 'Result':
                        bool = 1
                        # save this pod as result
                        results = wolframalpha.Pod(item)
                # if we've found a good result        
                if bool:
                    # set output to the text of results
                    # this could be made prettier, not sure how though
                    streng = (results).text
                else:
                    # if no primary/Result flag, not found.
                    # just take the output and send as results
                    # allows answering/definitions of more vague requests
                    print("Not found")
                    for pod in res.pods:
                        for sub in pod.subpods:
                            # concatenate the output string
                            streng = streng + sub.text
            # occurs when WA cant interpret query
            except (AttributeError):
                print("Invalid message")
                unknownList = ["I don't understand that.", "Maybe for some peanut-butter"]
                streng = unknownList[random.randint(0, len(unknownList)-1)]
                #streng = "I don't understand that query."
            # send the output message
            await client.send_message(message.channel, message.author.mention + '\r\n' + streng, tts=ttsbool)

blacklist = Blacklist('blacklist.txt')
playlists = Playlists('playlists.txt')
client.run(token)
