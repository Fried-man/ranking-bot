import discord
import re
import math
from datetime import datetime

intents = discord.Intents().all()
client = discord.Client(prefix='', intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.content.startswith('/'):
            #theContent = message
            await message.delete()
            if message.content == '/help':
                await message.channel.send('List of commands:\n- "/log" copies all non bot messages\n- "/clean" deletes all of my messages and left over commands\n- "/rank them" updates #stats\n- "/snitch" DM\'s people for their unformatted #scoreboard entries')
            elif message.content == '/log':
                edhRanked = headerMaker("EDH / Commander Games")
                messages = await message.channel.history(limit=1000).flatten()
                messages.reverse()
                messages = messageToArray(messages)
                for num, game in enumerate(messages, start = 1): # go through each game
                    edhRanked += str(num).rjust(3, '0') + "  "
                    for position in game[1:]:
                        edhRanked += str(position[0]) + ") "
                        for player in position[1:]:
                            currPlayer = message.guild.get_member(user_id=int(player[3:].strip(">")))
                            if currPlayer is None: # user left server
                                currPlayer = await client.fetch_user(user_id=int(player[3:].strip(">")))
                                currPlayer = currPlayer.name
                            else:
                                currPlayer = currPlayer.display_name
                            edhRanked += "***`" + currPlayer + "`*** "
                    edhRanked += "\n"
                for x in messageTruncate(edhRanked):
                    await message.channel.send(x) # send results to #stats
                    x = 0
            elif message.content == '/clean':
                messages = await message.channel.history(limit=1000).flatten()
                for x in messages:
                    if x.author == client.user or x.content.startswith('/'):
                        await x.delete()
            elif message.content == '/new game':
                response = "Who is playing?\n"
            elif message.content == '/snitch':
                if message.channel.id == 713227906725183508:
                    messages = await message.channel.history(limit=1000).flatten() # read through all messages in channel
                    messages.reverse()
                    for log in messages:
                        if log.author == client.user:
                            continue
                        logContent = log.content
                        if not logContent.startswith('X-Mage, Commander:') and not logContent.startswith('X-Mage, Draft'): # check if !legit edh game
                            logContent = "`" + logContent + "`\n -You\n\nThis makes zero sense to me asshole. Stop being a pleb and start your shit with \"X-Mage, Commander:\" or delete your spam. If there is an issue or a new game mode just contact <@!264196467403522048> for help."
                            print(logContent)
                            if log.author.dm_channel is None:
                                await log.author.create_dm()
                            await log.author.dm_channel.send(logContent)
            elif message.content == '/rank them':
                inputChannel = discord.utils.get(message.guild.channels, id=713227906725183508) # setup #scoreboard
                messages = await inputChannel.history(limit=1000).flatten() # read through all messages in channel
                messages.reverse()
                messages = messageToArray(messages)
                scores = []
                scores.append(["Overall Rankings", rankGames(messages)])
                monthly = []
                for game in messages:
                    Found = False
                    game[0] = str(game[0].strftime("%B - %Y"))
                    for month in monthly:
                        if game[0] == month[0]:
                            Found = True
                            month[1].append(game)
                    if Found is False:
                        monthly.append([game[0], [game]])
                #print("\n\n\n")
                for month in monthly:
                    print(month)
                    scores.append([month[0], rankGames(month[1])])
                #print("\n\n\n")
                outputChannel = discord.utils.get(message.guild.channels, id=732452709101469757) # setup #stats
                messages = await outputChannel.history(limit=1000).flatten() # read all messages in #stats
                for x in messages: # go through recorded messages
                    if x.author == client.user or x.content.startswith('/'): # find any comment from bot or old commands
                        await x.delete() # delete them
                for mode in scores:
                    #print(mode[1][0][1])
                    #print(mode[1][1])
                    #print(mode[1][0][1][0][3:len(mode[1][0][1][0]) - 1])
                    for player in mode[1][0]: # go through ranked players
                        #print("this is the message: " + str(player[0][3:len(player[0]) - 1]))
                        currPlayer = message.guild.get_member(user_id=int(player[0][3:].strip(">")))
                        if currPlayer is None: # user left server
                            currPlayer = await client.fetch_user(user_id=int(player[0][3:].strip(">")))
                            player[0] = currPlayer.name
                        else:
                            player[0] = currPlayer.display_name
                    for player in mode[1][1]: # go through unranked players
                        currPlayer = message.guild.get_member(user_id=int(player[0][3:].strip(">")))
                        if currPlayer is None: # user left server
                            currPlayer = await client.fetch_user(user_id=int(player[0][3:].strip(">")))
                            player[0] = currPlayer.name
                        else:
                            player[0] = currPlayer.display_name
                    for x in messageTruncate(printRanking(mode[0], mode[1])):
                        await outputChannel.send(x) # send results to #stats
            else:
                print(message.content)
                await message.channel.send('The command "' + message.content + '" is unkown to me. Type "/help" for a list of commands')

def printRanking(dataName, cleanData):
    outputText = headerMaker(dataName)
    outputText += "* Games needed to qualify: " + str(cleanData[2]) + "\n\n"
    print("\n\n\n\n\n\n")
    tiedData = []
    for i in range(0, len(cleanData[0])):
        rank = [cleanData[0][i]]
        j = 1
        while i+j < len(cleanData[0]) and cleanData[0][i][3] == cleanData[0][i+j][3]:
            rank.append(cleanData[0][i+j])
            j += 1
        #i = i+j
        print(rank)
        #print(cleanData[0][i-1][3])
        if i == 0 or cleanData[0][i-1][3] != cleanData[0][i][3]:
            tiedData.append(rank)
    for i in range(0, len(tiedData)): # for each ranked player
        for rankedPlayer in tiedData[i]:
            tiePush = 0
            for rank in tiedData[:i]:
                tiePush += len(rank) - 1
            outputText += playerStats(rankedPlayer, str(i + 1 + tiePush))
    for unrankedPlayer in cleanData[1]: # for each unranked player
        outputText += playerStats(unrankedPlayer, "Unranked")
    return outputText

def playerStats(player, rank):
    #print(player)
    stats = "***`" + rank + ") " + player[0] + "`***\n" # first line
    stats += '    - Calculated Score: ' + str(round(player[3], 2)) + '\n' #second line
    stats += '    - Games Played & Recorded: ' + str(player[2]) + '\n' #third line
    stats += '    - Total Score: ' + str(player[1]) + '\n' # fourth line
    for j in range(4, len(player)):
        if player[j][1] != 0:
            stats += '    - ' + str(player[j][0]) + ' person game ending positions: ( '
            for k in range(2, len(player[j]) - 1):
                stats += str(player[j][k]) + ' - '
            stats += str(player[j][len(player[j]) - 1]) + ' )\n'
    return stats

def headerMaker(dataName):
    outputText = '-------------------------------------------------------------------\n'
    outputText += dataName.upper().center(82) + '\n-------------------------------------------------------------------\n'
    return outputText

def messageTruncate(inputString): # Makes string into multiple messages
    maxLength = 1500 # This number doesnt error but not sure if its the max
    if len(inputString) < maxLength: # Truncate not needed case
        return [inputString] # return original massage as list
    inputString = inputString.split("\n") # split by line
    arrayVersion = [] # output message list
    temp = "" # current message
    while len(inputString) > 0: # add until no lines left
        if len(temp + inputString[0] + "\n") < maxLength: # message not too long
            temp += inputString[0] + "\n"
            inputString.pop(0) # remove first line
        else: # need to store current message and move to next one
            arrayVersion.append(temp[:-2]) # removes extra \n
            temp = ""
    if len(temp) > 0: # add leftover goodies to end of message list
        arrayVersion.append(temp[:-2])
    return arrayVersion # return list of shorter strings so discord isnt mad

def messageToArray(inputMessages):
    edhRanked = []
    for i in range(0, len(inputMessages)): # go through each game
        x = inputMessages[i] # str(x.created_at)
        tempDate = x.created_at
        x, sep, tail = x.content.partition('*') # delete any end-game comments
        if x.startswith('X-Mage, Commander:'): # check if legit edh game
            tempGame = [tempDate]
            x = re.split('\)', x) # split up by ranking
            for y in range(1, len(x)): # for each ranking y++
                x[y] = x[y].split() # split tied players up and segregate unnecessary text
            x = [[i for i in nested if '<' in i and '>' in i] for nested in x]
            for y in range(1, len(x)): # for each ranking y++
                tiePush = 0
                for i in range(0, y): # iterate through players
                    tiePush += len(x[i]) - 1
                tempPosition = [y + tiePush + 1]
                for z in x[y]: # each player in section
                    tempPosition.append(z)
                tempGame.append(tempPosition)
            edhRanked.append(tempGame)
    return edhRanked

def rankGames(messages):
    scores = [] # setup intial value for array
    for game in messages: # go through each game
        totalPlayers = str(game).count('<')
        for position in range(1, len(game)):
            for participant in game[position][1:]:
                found = False
                for player in scores: # check if player is already added to scoring array
                    backToNormal = 0
                    for playerAfter in range(1, len(game[position][1:])):
                        backToNormal += playerAfter
                    score = ((totalPlayers - game[position][0] + 1) * len(game[position][1:]) - backToNormal) / len(game[position][1:])
                    if player[0] == participant: # player was added in previous game
                        found = True # change first entry status to true
                        player[1] += score # add score to total score
                        player[2] += 1 # add 1 to total game
                        for i in range(4, 3 + totalPlayers):
                            if i > len(player):
                                newThing = [i - 3,0]
                                for j in range(1, i - 3 + 1): # add all places
                                    newThing.append(0)
                                newPlayer.append(newThing)
                        if len(player) <= totalPlayers + 2: # never played with this many players
                            multiScore = [totalPlayers, 0]
                            for i in range(2, totalPlayers + 2): # add all places
                                multiScore.append(0)
                            multiScore[game[position][0] + 1] = 1
                            player.append(multiScore)
                        else:
                            player[totalPlayers + 2][position + 1] += 1
                        player[totalPlayers + 2][1] += 1
                if found is False: # first game for the player
                    backToNormal = 0
                    for playerAfter in range(1, len(game[position][1:])):
                        backToNormal += playerAfter
                    score = ((totalPlayers - game[position][0] + 1) * len(game[position][1:]) - backToNormal) / len(game[position][1:])
                    newPlayer = [participant, score, 1, 0] # name, total score, total games, final score
                    for i in range(4, 3 + totalPlayers):
                        if i > len(newPlayer):
                            newThing = [i - 3,0]
                            for j in range(1, i - 3 + 1): # add all places
                                newThing.append(0)
                            newPlayer.append(newThing)
                    multiScore = [totalPlayers, 1]
                    for i in range(2, totalPlayers + 2): # add all places
                        multiScore.append(0)
                    multiScore[game[position][0] + 1] = 1
                    newPlayer.append(multiScore)
                    scores.append(newPlayer) # copy paste values from first game into scoring array
        #for x in scores:
        #    print(x)
        #print("\n\n")
    finalData = [[],[],0]
    scores.sort(key=lambda x: x[2]) # rank them by total games
    scores.reverse()
    finalData[2] = math.floor(scores[0][2]  * .25)
    for player in scores:
        player[3] = (player[1] / float(player[2])) # divide total score by total games
        if player[2] >= finalData[2]: # check for game threshold
            finalData[0].append(player)
        else:
            finalData[1].append(player)
    finalData[0].sort(key=lambda x: x[3]) # rank them by score
    finalData[0].reverse() # reverse to have #1 be first
    return finalData

client.run('???')
