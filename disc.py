import discord
from discord.ext import commands
import random
import math
import time
import asyncio
from lxml import html, etree   #python -m pip install lxml
import requests
import json


try:
    description = '''Welcome to Alo-Bot! Someone teach me how to code this junk'''
    bot = commands.Bot(command_prefix='?', description=description)

    @bot.event
    async def on_ready():
        print('Logged in as')
        print(bot.user.name)
        print(bot.user.id)
        print('------')
        await bot.change_presence(game=discord.Game(name='with your feelings :^)'))

    ''' QUICK MAFS'''
    @bot.command()
    async def add(a:float, b:float, member: discord.Member = None):
        if(member != None):
            await bot.say(f'pong <@{member.id}>')
            await bot.say(a+b)
        else:
            await bot.say(a+b)
        
    @bot.command()
    async def sub(a:float, b:float):
        await bot.say(a-b)

    @bot.command()
    async def times(a:float, b:float):
        await bot.say(a*b)

    @bot.command()
    async def divide(a:float, b:float):
        await bot.say(a/b)

    @bot.command()
    async def sq(a:float, b = None):
        if b == None:
            await bot.say(a*a)
        else:
            await bot.say(a**float(b))

    @bot.command()
    async def sqrt(a:float):
        await bot.say(math.sqrt(a))
        

    '''BNS STUFF'''
    
    @bot.command()
    async def pts():
        rng = random.randint(0,1)
        if rng == 0:
            await bot.reply("You have SUCCESSFULLY transmuted a PTS! RNGesus shines its lights upon you!")
        else:
            await bot.reply("You prayed to the wrong god!")

    @bot.command()
    async def bns(*args):
        if len(args) == 1:
            page = requests.get('http://na-bns.ncsoft.com/ingame/bs/character/profile?c='+args[0]+'&s=103')
        elif (len(args) == 2 and args[0]!= "na" and args[0] != "eu"):
            page = requests.get('http://na-bns.ncsoft.com/ingame/bs/character/profile?c='+args[0]+'%20'+args[1]+'&s=103')
        elif (len(args) == 2):
            page = requests.get('http://'+args[0]+'-bns.ncsoft.com/ingame/bs/character/profile?c='+args[1]+'&s=103')
        elif (len(args) == 3):
            page = requests.get('http://'+args[0]+'-bns.ncsoft.com/ingame/bs/character/profile?c='+args[1]+'%20'+args[2]+'&s=103')
        else:
            await bot.reply("WRONG SYNTAX BOIIIII")
            return
        tree = html.fromstring(page.content)
        charName = tree.xpath('//*[@id="header"]/dl/dt/span/text()')#//dl//span[@class = "name"]/text()
        
        accName = tree.xpath('//dl//a[@href = "#"]/text()')
        charDesc = tree.xpath('//dd[@class = "desc"]//li/text()')
        img = tree.xpath('//*[@id="contents"]/section/div[1]/div[1]/img/text()')
        
        attack = tree.xpath('//*[@id="total-int_attack_power_value"]/text()')
        
         # index 0 = class, 1 = Level, 2 = (nothing) , 3= server, 4 = faction + faction rank, 5 = clan
        charHMLevel = tree.xpath('//dd[@class = "desc"]//li//span[@class = "masteryLv"]/text()')

        
        await bot.say("Account Name: "+accName[0]+"\nCharacter Name: **"+charName[0]+"**"+"\nClan: **"+charDesc[5]+"**")
        await bot.say(charDesc[0]+" "+charDesc[1]+" "+charHMLevel[0]+"\n"+charDesc[3]+" "+charDesc[4])
        await bot.say(str(attack))

    @bot.command()
    async def tt():
        """ TT schedule """
        await bot.say("Next TT: Sunday 8:30PM")
    @bot.command()
    async def vt():
        """ VT schedule """
        await bot.say("VT whenever")
    @bot.command()
    async def bt():
        """ BT schedule """
        await bot.say("We don't do that here")
        
    '''Fun Stuff'''
    
    @bot.command()
    async def about():
        em = discord.Embed(title='*About Me*', description='''Welcome to Alo-Bot! This bot doesn't do jack shit''', colour=0x42eef4)
        em.add_field(name="Created by:", value="<@134071680359202816>", inline=True)
        em.add_field(name="Twitch:", value="https://www.twitch.tv/alo666", inline=False)
        em.add_field(name="BNS Profile:", value="http://na-bns.ncsoft.com/ingame/bs/character/profile?c=Aloran&s=103")
        await bot.say(embed=em)
    @bot.command(pass_context=True)
    
    async def play(ctx, url):
        while(bot.is_voice_connected(discord.Server) == True):
            await bot.disconnect()
        author = ctx.message.author
        voice_channel = author.voice_channel
        vc = await bot.join_voice_channel(voice_channel)
        player = await vc.create_ytdl_player(url)
        player.start()
        await bot.say("Playing something in the **"+str(voice_channel)+"** channel")
        
    @bot.command(pass_context = True)
    async def leave(ctx):
        for x in bot.voice_clients:
            if(x.server == ctx.message.server):
                return await x.disconnect()
        
    '''FortNite Guns'''
    @bot.command()
    async def fort(*args):
        name = '%20'.join(args)
        URL = 'https://masterfortnite.com/player/pc/'+name
        
       # URL = 'https://api.fortnitetracker.com/v1/profile/pc/'+name
        #headers = {"TRN-Api-Key": "f8e16f0e-927e-4b54-afa5-2ac33e1dfaca"}
        page = requests.get(URL)
        #result = page.text
        tree = html.fromstring(page.content)
        
        totalGames = tree.xpath('/html/body/div[4]/div/div[1]/div[1]/div/div[1]/div/div/div[2]/text()')
        totalKills = tree.xpath('/html/body/div[4]/div/div[1]/div[1]/div/div[2]/div/div/div[4]/div[2]/text()')
        totalWins = tree.xpath('/html/body/div[4]/div/div[1]/div[1]/div/div[2]/div/div/div[5]/div[2]/text()')
        winRate = tree.xpath('/html/body/div[4]/div/div[1]/div[1]/div/div[2]/div/div/div[1]/div[2]/text()')
        KD = tree.xpath('/html/body/div[4]/div/div[1]/div[1]/div/div[2]/div/div/div[2]/div[2]/text()')
        
        await bot.say('Total Wins: **' +totalWins[0]+'**\nKD: '+KD[0]+'\nWin Rate: '+winRate[0]+'\nGames Played: '+totalGames[0]+'\nKills: '+totalKills[0])
        
        #wins = tree.xpath('//*[@id="profile"]/div[4]/div/div[3]/div/div[1]/div[2]/text()')
        #await bot.say(len(wins))

    
    @bot.command()
    async def ar():
        """ -> Shows the stats of all Assualt Rifles."""
        em = discord.Embed(title = "Assault Rifles", description = "Body / Head / Reload Time", colour=0x42eef4)
        em.add_field(name = "\a" , value = "\a", inline = False)
        em.add_field(name = "Gray" , value = " 30 / **60** / 2.3s", )
        em.add_field(name = "Green" , value = " 31 / **62** / 2.2s")
        em.add_field(name = "Blue" , value = " 33 / **66** / 2.2s")
        em.add_field(name = "\a" , value = "\a", inline = False)
        em.add_field(name = "Purple" , value = " 35 / **70** / 2.1s")
        em.add_field(name = "Gold" , value = " 36 / **72** / 2.1s")
        em.add_field(name = "\a" , value = "\a")
        await bot.say(embed = em)
        
    @bot.command()
    async def burst():
        """ -> Shows the stats of all Burst Assualt Rifles."""
        em = discord.Embed(title = "**Burst Assault Rifles**", description = "Body / Head / Reload Time", colour=0x42eef4)
        em.add_field(name = "\a" , value = "\a", inline = False)
        em.add_field(name = "Gray" , value = " 27 / **54** / 2.9s", )
        em.add_field(name = "Green" , value = " 29 / **58** / 2.7s")
        em.add_field(name = "Blue" , value = " 30 / **60** / 2.6s")
        em.add_field(name = "\a" , value = "\a", inline = False)
        em.add_field(name = "Purple" , value = " 32 / **64** / 2.5s")
        em.add_field(name = "Gold" , value = " 33 / **66** / 2.3s")
        em.add_field(name = "\a" , value = "\a")
        await bot.say(embed = em)
        
    @bot.command()
    async def sniper():
        """ -> Shows the stats of all Snipers."""
        em = discord.Embed(title = "**Sniper Rifles**", description = "Body / Head / Reload Time", colour=0x42eef4)
        em.add_field(name = "\a" , value = "\a", inline = False)
        em.add_field(name = "Green Hunting" , value = " 86 / **215** / 1.9s")
        em.add_field(name = "Blue Hunting" , value = " 90 / **225** / 1.8s")
        em.add_field(name = "\a" , value = "\a")
        em.add_field(name = "\a" , value = "\a", inline = False)
        em.add_field(name = "Blue Bolt" , value = " 105 / **262.5** / 3.0s")
        em.add_field(name = "Purple Bolt" , value = " 110 / **275** / 2.8s")
        em.add_field(name = "Gold Bolt" , value = " 116 / **290** / 2.7s")
        em.add_field(name = "\a" , value = "\a", inline = False)
        em.add_field(name = "Purple Semi" , value = " 63 / **157.5** / 2.5s")
        em.add_field(name = "Gold Semi" , value = " 66 / **165** / 2.3s")
        em.add_field(name = "\a" , value = "\a")
        await bot.say(embed = em)
        
    @bot.command()
    async def shotgun():
        
        """ -> Shows the stats of all Shotguns. """
        em = discord.Embed(title = "Shotguns", description = "Body / Head / Reload Time", colour=0x42eef4)
        em.add_field(name = "\a" , value = "\a", inline = False)
        em.add_field(name = "Gray Tactical" , value = " 67 / **134** / 6.3s", )
        em.add_field(name = "Green Tactical" , value = " 70 / **140** / 6.0s")
        em.add_field(name = "Blue Tactical" , value = " 74 / **148** / 5.7s")
        em.add_field(name = "\a" , value = "\a", inline = False)
        em.add_field(name = "Green Pump" , value = " 80 / **160** / 4.8s")
        em.add_field(name = "Blue Pump" , value = " 85 / **170** / 4.6s")
        em.add_field(name = "\a" , value = "\a")
        em.add_field(name = "\a" , value = "\a", inline = False)
        em.add_field(name = "Purple Heavy" , value = " 73.5 / **183.75** / 5.9s")
        em.add_field(name = "Gold Heavy" , value = " 77 / **192.5** / 5.6s")
        em.add_field(name = "\a" , value = "\a")
        await bot.say(embed = em)
        
    @bot.command()
    async def smg():
        """ -> Shows the stats of all SMGs."""
        em = discord.Embed(title = "**Sub Machine Guns**", description = "Body / Head / Reload Time", colour=0x42eef4)
        em.add_field(name = "\a" , value = "\a", inline = False)
        em.add_field(name = "Gray Silenced" , value = " 22 / **44** / 2.2s")
        em.add_field(name = "Green Silenced" , value = " 23 / **46** / 2.1s")
        em.add_field(name = "Blue Silenced" , value = " 24 / **48** / 2.0s")
        em.add_field(name = "\a" , value = "\a", inline = False)
        em.add_field(name = "Green Tact" , value = " 18 / **36** / 2.4s")
        em.add_field(name = "Blue Tact" , value = " 19 / **38** / 2.3s")
        em.add_field(name = "Purple Tact" , value = " 20 / **40** / 2.2s")
        em.add_field(name = "\a" , value = "\a", inline = False)
        em.add_field(name = "Green Drum" , value = " 26 / **52** / 3.2s")
        em.add_field(name = "Blue Drum" , value = " 27 / **54** / 3.0s")
        em.add_field(name = "\a" , value = "\a")
        await bot.say(embed = em)
                
    '''RNGesus'''

    @bot.command()
    async def roll(a:int, b = None):
        if b == None:
            await bot.say(random.randint(0, a))
        else:
            await bot.say(random.randint(a,int(b)))
        
    @bot.command()
    async def choose(*choices : str):
        """ -> Chooses between multiple choices."""
        result = random.choice(choices)
        await bot.say("RNGesus says: "+result.title())

    fortniteLocations = ["Lazy Links","Dusty Divot","Fatal Fields","Flush Factory","Greasy Grove","Haunted Hills",
                         "Junk Junction","Lonely Lodge","Loot Lake","Lucky Landing","Moisty Mire","Pleasant Park","Retail Row",
                         "Risky Reels","Salty Springs","Shifty Shafts","Snobby Shores","Tilted Towers","Tomato Town","Wailing Woods",
                         "Paradise Palms", "Pirate Ship"]
    @bot.command(description = 'You wanna know where to drop?')
    async def drop(a = None):
        if a == None:
            await bot.say("You should drop at __**"+random.choice(fortniteLocations)+"**__!")
        else:
            tempList = []
            for i in range(int(a) - 1):
                tempList.append(random.choice(fortniteLocations))
            await bot.say("You should drop at "+', '.join(map('__**{}**__'.format, tempList))+" or __**"+random.choice(fortniteLocations)+"**__!")
     


    @bot.command()
    async def timer(sec : float):
        """ -> set a timer for T seconds """
        await bot.reply("setting a timer for "+str(sec)+" seconds")
        time.sleep(sec-0.5)
        await bot.reply("Time's Up!")


    @bot.command()
    async def repeat(times : int, *content):
        """ -> Repeats a message multiple times (Max 80)"""
        if times > 80:
            await bot.reply("you trying to break me you dumb bitch?")
        else:
            x = ''
            for i in range(times):
                x = x + (' '.join(map(str,content))) + ' '
                
            await bot.say(x)

    @bot.command()
    async def repeatTriangle(times: int, *content):
        if times > 15:
            await bot.reply("no")
        else:
            x=''
            for i in range(times):
                x = x + (' '.join(map(str,content)))+' '
                time.sleep(0.5)
                await bot.say(x)

    @bot.command()
    async def joined(member : discord.Member):
        """Says when a member joined."""
        await bot.say('{0.name} joined in {0.joined_at}'.format(member))

    @bot.group(pass_context=True)
    async def cool(ctx):
        """ -> Says if a user is cool.
        In reality this just checks if a subcommand is being invoked.
        """
        if ctx.invoked_subcommand is None:
            await bot.say('No, {0.subcommand_passed} is not cool'.format(ctx))

    @cool.command(name='bot')
    async def _bot():
        """Is the bot cool?"""
        await bot.say('Yes, the bot is cool.')

    @bot.command(pass_context=True)
    async def test(ctx):
        msg = 'testing'
        await bot.say(msg)
        await bot.edit_message(discord.Channel,'tester')    
except:
    pass

bot.run('redacted')


