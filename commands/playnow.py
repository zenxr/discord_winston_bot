    # !pause, currently unfinished
    # function is to have the bot ignore input
    # until owner says resume/unpause
    # to dequeue all songs in MusicBot and instantly play a song
from discord.message import Message

def playnow(message):
    query = message.content
    await client.send_message(message.channel, "!clear")
    await client.send_message(message.channel, "!play " + query.split(' ', 1)[1])