import discord
import re
import math

client = discord.Client()

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
                await message.channel.send('List of commands:\n- "/log" copies all non bot messages\n- "/clean" deletes all of my messages and left over commands\n- "/rank them" updates #stats')
            elif message.content == '/log':
                edhRanked = headerMaker("EDH / Commander Games")
                messages = await message.channel.history(limit=1000).flatten()
                messages.reverse()
                for i in range(0, len(messages)): # go through each game
                    x = messages[i] # str(x.created_at)
                    x, sep, tail = x.content.partition('*') # delete any end-game comments
                    if x.startswith('X-Mage, Commander:'): # check if legit edh game
                        edhRanked += str(i + 1).rjust(3, '0') + "  "
                        x = re.split('\)', x) # split up by ranking
                        for y in range(1, len(x)): # for each ranking y++
                            x[y] = x[y].split() # split tied players up and segregate unnecessary text
                        x = [[i for i in nested if '<' in i and '>' in i] for nested in x]
                        for y in range(1, len(x)): # for each ranking y++
                            tiePush = 0
                            for i in range(0, y): # iterate through players
                                tiePush += len(x[i]) - 1
                            edhRanked += str(y + tiePush + 1) + ") "
                            for z in x[y]: # each player in section
                                edhRanked += z + " "
                        edhRanked += "\n"
                for x in messageTruncate(edhRanked):
                    await message.channel.send(x) # send results to #stats
            elif message.content == '/clean':
                messages = await message.channel.history(limit=1000).flatten()
                for x in messages:
                    if x.author == client.user or x.content.startswith('/'):
                        await x.delete()
            elif message.content == '/new game':
                response = "Who is playing?\n"
            elif message.content == '/rank them':
                inputChannel = discord.utils.get(message.guild.channels, id=713227906725183508) # setup #scoreboard
                messages = await inputChannel.history(limit=1000).flatten() # read through all messages in channel
                messages.reverse() # put them in chronological order
                scores = [["",0,0]] # setup intial value for array
                counterduh = 0
                for x in messages: # go through each game
                    x, sep, tail = x.content.partition('*') # delete any end-game comments
                    totalPlayers = x.count('<')
                    if x.startswith('X-Mage, Commander:'): # check if legit edh game
                        x = re.split('\)', x) # split up by ranking
                        totalCounted = 0
                        for y in range(1, len(x)): # for each ranking y++
                            x[y] = x[y].split() # split tied players up and segregate unnecessary text
                            tiedCounter = 0
                        x = [[i for i in nested if '<' in i and '>' in i] for nested in x]
                        x.remove(x[0])
                        for y in range(0, len(x)): # for each ranking y++
                            for z in x[y]: # for each item in subarray (rank is common thread)
                                totalCounted += 1
                                tiePush = 0
                                for i in range(0, y): # iterate through players
                                    tiePush += len(x[i]) - 1
                                found = False # assume first entry for player
                                for player in scores: # check if player is already added to scoring array
                                    if player[0] == z: # player was added in previous game
                                        found = True # change first entry status to true
                                        player[1] += len(x) - y # add score to total score
                                        player[2] += 1 # add 1 to total game
                                        for i in range(4, 3 + totalPlayers):
                                            if i > len(player):
                                                newThing = [i - 3,0]
                                                for j in range(1, i - 3 + 1): # add all places
                                                    newThing.append(0)
                                                newPlayer.append(newThing)
                                        #print(player[len(player)-1][0])
                                        if len(player) <= totalPlayers + 2: # never played with this many players
                                            multiScore = [totalPlayers, 0]
                                            for i in range(2, totalPlayers + 2): # add all places
                                                multiScore.append(0)
                                            multiScore[y + 2 + tiePush] = 1
                                            player.append(multiScore)
                                        else:
                                            #print(player[totalPlayers + 3])
                                            #print(player)
                                            #print(player[totalPlayers + 2])
                                            player[totalPlayers + 2][y + 2 + tiePush] += 1
                                        player[totalPlayers + 2][1] += 1
                                if found is False: # first game for the player
                                    newPlayer = [z, len(x) - y, 1, 0] # name, position, total games, final score
                                    for i in range(4, 3 + totalPlayers):
                                        if i > len(newPlayer):
                                            newThing = [i - 3,0]
                                            for j in range(1, i - 3 + 1): # add all places
                                                newThing.append(0)
                                            newPlayer.append(newThing)
                                    multiScore = [totalPlayers, 1]
                                    for i in range(2, totalPlayers + 2): # add all places
                                        multiScore.append(0)
                                    multiScore[y + 2 + tiePush] = 1
                                    newPlayer.append(multiScore)
                                    #print(newPlayer)
                                    scores.append(newPlayer) # copy paste values from first game into scoring array
                                    #scores[len(scores)-1][1] += 1
                            #else:
                            #    x[y].remove(z)
                        counterduh += 1
                        print(counterduh)
                        for x in scores[1:]:
                            print(x)
                        print("\n\n")
                scores.remove(scores[0]) # remove first item in scoring array (its blank)
                #print(scores)
                for player in scores: # go through tracked players
                    player[3] = (player[1] / float(player[2])) # divide total score by total games
                #print(scores)
                scores.sort(key=lambda x: x[3]) # rank them by score
                scores.reverse() # reverse to have #1 be first
                outputChannel = discord.utils.get(message.guild.channels, id=732452709101469757) # setup #stats
                messages = await outputChannel.history(limit=1000).flatten() # read all messages in #stats
                for x in messages: # go through recorded messages
                    if x.author == client.user or x.content.startswith('/'): # find any comment from bot or old commands
                        await x.delete() # delete them
                #await outputChannel.send(printRanking("Overall Rankings", scores)) # send results to #stats
                for x in messageTruncate(printRanking("Overall Rankings", scores)):
                    await outputChannel.send(x) # send results to #stats
            else:
                await message.channel.send('The command "' + message.content + '" is unkown to me. Type "help" for a list of commands')

def printRanking(dataName, cleanData):
    outputText = headerMaker(dataName)
    for i in range(0, len(cleanData)): # for each item in scoring array i++
        player = cleanData[i] # player array being set
        print(player)
        outputText += str(i + 1) + ") " + player[0] + "\n" # first line
        outputText += '    - Calculated Score: ' + str(round(player[3], 2)) + '\n' #second line
        outputText += '    - Games Played & Recorded: ' + str(player[2]) + '\n' #third line
        outputText += '    - Total Score: ' + str(player[1]) + '\n' # fourth line
        for j in range(4, len(player)):
            if player[j][1] != 0:
                outputText += '    - ' + str(player[j][0]) + ' person game ending positions: ( '
                for k in range(2, len(player[j]) - 1):
                    outputText += str(player[j][k]) + ' - '
                outputText += str(player[j][len(player[j]) - 1]) + ' )\n'
    return outputText

def headerMaker(dataName):
    outputText = '-------------------------------------------------------------------\n'
    outputText += dataName.upper().center(82) + '\n-------------------------------------------------------------------\n'
    return outputText

def messageTruncate(inputString):
    maxLength = 1999
    if len(inputString) < maxLength:
        return [inputString[0:int(len(inputString))]]
    arrayVersion = []
    i = 0 # starting character for message
    while (len(arrayVersion) + 1) * maxLength < len(inputString):
        for j in range(maxLength * (len(arrayVersion) + 1), 0, -1): # by end of max message
            if inputString[j-1:j] == "\n": # find new closest new line
                arrayVersion.append(inputString[i:j])
                i = j
                break
    arrayVersion.append(inputString[i:len(inputString)])
    return arrayVersion

client.run('NzMyNTI2MjIzNzEyMDU5NTA0.Xw9Kiw.nSmUfNGpQVoBNWR4Dv0bdK_0aX4')
