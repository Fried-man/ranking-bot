import discord
import re

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
                messages = await message.channel.history(limit=1000).flatten()
                #await message.channel.send(str(messages))
                messages.reverse()
                for x in messages:
                    await message.channel.send(str(x.created_at) + " | " + str(x.content))
                    print(str(x.created_at) + " | " + str(x.content))
                #print(str(messages))
            elif message.content == '/clean':
                messages = await message.channel.history(limit=1000).flatten()
                for x in messages:
                    if x.author == client.user or x.content.startswith('/'):
                        await x.delete()
            elif message.content == '/rank them':
                inputChannel = discord.utils.get(message.guild.channels, id=713227906725183508) # setup #scoreboard
                messages = await inputChannel.history(limit=1000).flatten() # read through all messages in channel
                messages.reverse() # put them in chronological order
                outputText = '--- Rankings ---\n' # set up header for ranking
                scores = [["",0,0]] # setup intial value for array
                for x in messages: # go through each game
                    x, sep, tail = x.content.partition('*') # delete any end-game comments
                    if x.startswith('X-Mage, Commander:'): # check if legit edh game
                        x = re.split('\)', x) # split up by ranking
                        for y in range(0, len(x)): # for each ranking y++
                            x[y] = x[y].split() # split tied players up and segregate unnecessary text
                            for z in x[y]: # for each item in subarray (rank is common thread)
                                if '<' in z and '>' in z: # check if item is a player
                                    #print(z, end = " ")
                                    found = False
                                    for player in scores: # check if player is already added to scoring array
                                        if player[0] == z: # player was added in previous game
                                            found = True
                                            player[1] += len(x) - y # add score to total score
                                            player[2] += 1 # add 1 to total game
                                    if found is False: # first game for the player
                                        scores.append([z, len(x) - y, 1]) # copy paste values from first game into scoring array
                        #print()
                scores.remove(scores[0]) # remove first item in scoring array (its blank)
                #print(scores)
                for player in scores: # go through tracked players
                    player[1] /= float(player[2]) # divide total score by total games
                #print(scores)
                scores.sort(key=lambda x: x[1]) # rank them by score
                scores.reverse() # reverse to have #1 be first
                for i in range(0, len(scores)): # for each item in scoring array i++
                    player = scores[i] # player array being set
                    outputText += str(i + 1) + ") " + player[0] + " - " + str(round(player[1], 2)) + "\n" # convert to readable format
                outputChannel = discord.utils.get(message.guild.channels, id=732452709101469757) # setup #stats
                messages = await outputChannel.history(limit=1000).flatten() # read all messages in #stats
                for x in messages: # go through recorded messages
                    if x.author == client.user or x.content.startswith('/'): # find any comment from bot or old commands
                        await x.delete() # delete them
                await outputChannel.send(outputText) # send results to #stats
            else:
                await message.channel.send('The command "' + message.content + '" is unkown to me. Type "help" for a list of commands')
            #await message.delete()
        

client.run('???')
