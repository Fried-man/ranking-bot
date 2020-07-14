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
                inputChannel = discord.utils.get(message.guild.channels, id=713227906725183508)
                messages = await inputChannel.history(limit=1000).flatten()
                messages.reverse()
                outputText = '--- Rankings ---\n'
                scores = [["",0,0]]
                for x in messages:
                    x, sep, tail = x.content.partition('*')
                    if x.startswith('X-Mage, Commander:'):
                        x = re.split('\)', x)
                        for y in range(0, len(x)):
                            x[y] = x[y].split()
                            for z in x[y]:
                                if '<' in z and '>' in z:
                                    #print(z, end = " ")
                                    found = False
                                    for player in scores:
                                        if player[0] == z:
                                            found = True
                                            player[1] += (len(x) - y)/float(len(x))
                                            player[2] += 1
                                    if found is False:
                                        newEntry = [z, (len(x) - y)/float(len(x)), 1]
                                        scores.append(newEntry)
                        #print()
                scores.remove(scores[0])
                #print(scores)
                for player in scores:
                    player[1] /= float(player[2])
                #print(scores)
                scores.sort(key=lambda x: x[1])
                scores.reverse()
                for i in range(0, len(scores)):
                    player = scores[i]
                    outputText += str(i + 1) + ") " + player[0] + " - " + str(round(player[1]*4, 2)) + "\n"
                outputChannel = discord.utils.get(message.guild.channels, id=732452709101469757)
                messages = await outputChannel.history(limit=1000).flatten()
                for x in messages:
                    if x.author == client.user or x.content.startswith('/'):
                        await x.delete()
                await outputChannel.send(outputText)
            else:
                await message.channel.send('The command "' + message.content + '" is unkown to me. Type "help" for a list of commands')
            #await message.delete()
        

client.run('???')
