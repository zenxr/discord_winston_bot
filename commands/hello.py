from discord.message import Message

def hello(message):
    return message.author.mention + '\r\n' + "Hello human."
