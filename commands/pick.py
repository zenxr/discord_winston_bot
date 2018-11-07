# pick heroes at random

from discord.message import Message
import random


# function to randomly select a hero, pass it a string
def pickAHero(category):
    attack = ["Doomfist", "Genji", "McCree", "Pharah", "Reaper", "Soldier76", "Sombra"]
    defense = ["Tracer", "Bastion", "Hanzo", "Junkrat", "Mei", "Torbjorn", "Widowmaker"]
    tank = ["D.Va", "Orisa", "Reinhardt", "Roadhog", "Winston", "Zarya"]
    support = ["Ana", "Lucio", "Mercy", "Symmetra", "Zenyatta", "Brigette", "Moira"]
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

def pick(message):
    m = splitmessage(message.content)
    if m[1] == "pick" and m[2] == "hero":
        # if message = "!winston pick hero"
        if len(m) == 3:
            hero = pickAHero("all")
            print("Picking hero : " + hero)
        else:
            # pick with the 4th word as the specified subtype of hero
            hero = pickAHero(m[3])
            print("Picking hero (" + m[3] + ") : " + str(hero))
        return message.author.mention + ' : ' + str(hero)
