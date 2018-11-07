import discord
import asyncio
import wolframalpha
import re
import random
import time
import json
import requests
import operator
import config
import classes.blacklist as Blacklist
import classes.playlist as Playlist

# import the commands module
from commands import *
# create a new client
client = discord.Client()
# secret token
token = config.token
# app_id for wolfram alpha API
app_id = config.app_id

# text-to-speech variable
ttsbool = False 

# my user ID for discord
ownerID = config.ownerID

gameStatus = "type !help for info"

# create a wolfram alpha client
clientWA = wolframalpha.Client(app_id)


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


# this runs when login successful
@client.event
async def wait_until_login():
    await client.change_presence(game=discord.Game(name=gameStatus))

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
    await client.change_presence(game=discord.Game(name=gameStatus))

# this runs when a member joins a server
# (only once, when they're invited)
@client.event
async def on_member_join(member):
    tmp = await client.send_message(member.server, "Welcome to the fam!\r\nType !help to check me out!")

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
    # temporarily adding a new 'admin' manually
    if blacklisted:
        if message.author.id != (ownerID or '1597242631655788161'):
            return

    # using the commands submodule
    if message.content.startswith('!winston hello'):
        await client.send_message(message.channel, hello.hello(message))
    if message.content.startswith('!winston pick'):
        await client.send_message(message.channel, pick.pick(message))

    # !help command
    if message.content.startswith('!help'):
        help_categories="1. Interaction with Lucio/MusicBot\r\n2. OverWatch commands\r\n3. Administration\r\n4. Other"
        embed = discord.Embed(title="**__Winston's Help Menu__**", description="I'm Winston. Ask me anything not in my commands and I'll try to answer! Respond with the number representing the category you'd like to see. Ex: 1")
        embed.add_field(name="Categories", value=help_categories, inline=False)
        helpMessagePrompt = await client.send_message(message.author, embed=embed)
        msg = await client.wait_for_message(author=message.author)
        if msg.content == '1' or msg.content == '2' or msg.content == '3' or msg.content == '4':
            # delete the previous help message
            await client.delete_message(helpMessagePrompt)
        if msg.content == '1':
            embed = discord.Embed(title="__**Interaction with Lucio/MusicBot**__")
            embed.add_field(name="!winston playlist show", value="Shows all saved playlists", inline=False)
            embed.add_field(name="!winston playlist add", value="Format: `!winston playlist add PLAYLISTNAME URL`\r\nSave a new playlist. Must be youtube or soundcloud." , inline=False)
            embed.add_field(name="!winston playlist remove", value="Format: `!winston playlist remove PLAYLISTNAME`\r\nRemove a saved playlist.", inline=False)
            embed.add_field(name="!playnow", value="Remove the current queue and play a song", inline=False)
            await client.send_message(message.author, "Send `!help` again to see other commands.", embed=embed)
        elif msg.content == '2':
            embed = discord.Embed(title="__**OverWatch Commands**__")
            embed.add_field(name="!player", value="Format: `!player Poseidon-12214`\r\nSearch OW API to look up top 5 heroes for a PC OverWatch player by their ID.", inline=False)
            embed.add_field(name="!winston pick hero", value="Format: `!winston pick hero`\r\nRandomly pick OverWatch heroes. Can pick by team, attack, defense, or offense by appending to the end of the command (!winston pick hero team)", inline=False)
            await client.send_message(message.author, "Send `!help` again to see other commands.", embed=embed)
        elif msg.content == '3':
            embed = discord.Embed(title="__**Administration**__")
            embed.add_field(name="!role list", value="Lists roles on this server", inline=False)
            embed.add_field(name="!role ROLENAME", value="Lists the permissions for a specific role on the server", inline=False)
            await client.send_message(message.author, "Send `!help` again to see other commands.", embed=embed)
        elif msg.content == '4':
            embed = discord.Embed(title="__**Other commands**__")
            embed.add_field(name="!help", value="Displays the help message", inline=False)
            embed.add_field(name="!winston hello", value="Prints a pretty response!", inline=False)
            embed.add_field(name="!cleanAll", value="Deletes 50 messages, regardless of author.", inline=False)
            await client.send_message(message.author, "Send `!help` again to see other commands", embed=embed)
    if message.content.startswith('!cleanAll'):
        deleted = await client.purge_from(message.channel, limit=50)
        await client.send_message(message.channel, 'Deleted {} message(s)'.format(len(deleted)))
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
    # to dequeue all songs in MusicBot and instantly play a song
    elif message.content.startswith('!playnow'):
        query = message.content
        await client.send_message(message.channel, "!clear")
        await client.send_message(message.channel, playnow.playnow(message))
 
    # !winston commands for wolframAlpha queries + special queries
    elif message.content.startswith('!winston'):
        # split message into a list of words
        m = splitmessage(message.content)
        
        # if doing stuff with user playlists
        if m[1] == "playlist":
            global playlists
            returnMsg = ""
            if m[2] == "show":
                embed = discord.Embed(title="__***DJ Winston***__", description="Use '!winston playlist NAME' to enqueue a playlist")
                pl = playlists.output_list()
                for line in pl:
                    splitlined = splitmessage(line)
                    returnMsg = returnMsg + "[" + splitlined[0] + "]" + "(" + splitlined[1] + ")\r\n"
                embed.add_field(name="Saved playlists:", value=returnMsg, inline=False)
                await client.send_message(message.channel, embed=embed)
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
                    await client.send_message(message.channel, "!clear")
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

blacklist = Blacklist.Blacklist('blacklist.txt')
playlists = Playlist.Playlists('playlists.txt')
client.run(token)
