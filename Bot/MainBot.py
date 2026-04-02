# Got this boiler plate from https://discordpy.readthedocs.io/en/stable/quickstart.html
import discord
import random
import asyncio
import spotipy
import lyricsgenius
from spotipy.oauth2 import SpotifyClientCredentials
import socket
import os
from discord.ext import tasks, commands

# CREATE A TEXT FILE IN YOUR BOT FOLDER NAMED d_token it should be .txt and paste discord token in that (ONE STRING NO NEWLINES)
f=open("d_token.txt", "r")
if f.mode == 'r':
    token = f.read()

# Array for storing command history
command_history = []

intents = discord.Intents.all()
client = commands.Bot(command_prefix='!',intents=intents)
intents.message_content = True
#Dictonary for listing out commands
command = {"!commands": "Lists out the commands available by the bot.",
           "!ping": "Pings the bot.",
            "!song [song title]": "Plays a song on the companion application.",
            "!poll: \"question\" \"option1\" \"option2\" \"option3\" \"option4\"": "Creates a poll with the given question and options.",
            "!recommend": "Recommends a song from the top 50 songs of the day in the U.S. on Spotify.",
            "!demographics": "Lists the server roles and the number of members in them.",
            "!lyrics [song title]": "Displays the song lyrics from Genius.",
            "!trivia":"Asks a music related trivia question."
            }
mod = {
    "!history": "Prints the command history of users.",
    "!mute @ member [reason]": "Mutes the given member with or without a reason.",
    "!unmute @ member": "Unmutes the given member.",
    "!kick @member": "Kicks the given member",
    "!ban @ member": "Bans the given member.",
}


# Command that will initiate the client connection to the server and pass a message to the companion app
@client.command()
async def song(ctx, *args):
    message = ' '.join(args)

    # Message current channel "Client initiating connection to server..."
    await ctx.send("Your message was: " + str(message))
    await ctx.send("Client initiating connection to server...")
    message = str(message)

    # Bot will function as the client
    ServerIP = "170.187.157.166"
    # Switch to below if you want to run locally
    # ServerIP = socket.gethostbyname(socket.gethostname())
    ServerPort = 12001
    ADDRESS = (ServerIP, ServerPort)

    # Create Client Socket
    try:
        ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print (f'Unable to establish a socket connection {err}\n')

    # Establish connection with the server
    try:
        ClientSocket.connect((ADDRESS))
        print ('Client connected to the server')
    except socket.error as err:
        print (f'Unable to connect to the server {err}')

    # Print Message to terminal
    print ("Sending to server: " + str(message))

    # Send the message to the server
    ClientSocket.send(message.encode())

    # Recieve the message from the server, print the message as confirmation
    message = ClientSocket.recv(1024)
    msg = message.decode()
    print ('Confirmation From Server: ' + str(msg))
    ClientSocket.close()

    # Message channel that connection has been closed
    await ctx.send("Confirmation from server: " + str(msg))
    await ctx.send("Connection to server closed, now available for commands")

#Pings the bot and sends response
@client.command()
async def ping(ctx):
    guild = ctx.guild
    embed = discord.Embed(
            title='Pong! 🏓',
            description=(f'Ping is {round(client.latency*1000)}ms.'),
            color = discord.Colour.blue()
        )
    await ctx.reply(embed=embed)

#Kicks a given user
@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
        print(f'Kicking {member}')
        await member.kick(reason=reason)
        kickEmbed=discord.Embed(
            title=f'User {member} has been kicked!',
        color=discord.Colour.blue()
        )
        await ctx.send(embed=kickEmbed)

#Bans a given user
@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    banEmbed=discord.Embed(
        title=f'User {member} has been banned!',
        color=discord.Colour.blue()
    )
    await ctx.send(embed=banEmbed)

@client.event
#The bot should not respond to itself
async def on_message(message):
    if message.author == client.user:
        return

    #If the test commands start with the same symbol as the bot command it throws an error so I changed it from ! -> ?
    if message.content.startswith('!commands'):
        commandList = ''
        for key in command:
            commandList += key + ": " + command[key] + "\n"
        modList = ''
        for key in mod:
            modList += key + ": " + mod[key] + "\n"

        embed = discord.Embed(
            title='Commands List',
            #description=commandList,
            color = discord.Colour.blue()
        )
        embed.add_field(name='', value='', inline=False)
        embed.add_field(name='Global Commands', value=commandList, inline=False)
        embed.add_field(name='', value='', inline=False)
        embed.add_field(name='Moderator Commands', value=modList, inline=False)
        await message.channel.send(embed=embed)

    #If the test commands start with the same symbol as the bot command it throws an error so I changed it from ! -> ?
    if message.content.startswith('?test'):
         await sendMessage(message.channel, "This is just a test message!")
    
    if message.content.startswith('?client'):
         print("Client called")
         # clientsocket.send(bytes("Hey there!!!","utf-8"));
    #if this line is removed the on_message event prevents all other client.commands to stop working
    await client.process_commands(message)

# Message that sends a welcome dm when somebody joins [TOGGLE OPTION FOR DM OPTION OR GENERAL CHANNEL PING]
@client.event
async def on_member_join(member):
    channel = member.guild.system_channel
    welcomeToggle= True
    welcomeEmbed = discord.Embed(
            title='Welcome!',
            description="Type !commands to get started with the bot!",
            color = discord.Colour.blue()
        )
    #while(welcomeToggle):
    await channel.send(member.mention,embed=welcomeEmbed)
    # for later use
    #else:
      #  await member.send(member.mention,embed=welcomeEmbed)


#here is a quick funcion that can send a message to a particular channel
async def sendMessage(channel, message):
     await channel.send(message)

# Add all user commands to the command_history array, followed by their username and the time the command was sent at
@client.event
async def on_command(ctx):
    command_history.append(ctx.message.content + " by " + ctx.author.name + " at " + str(ctx.message.created_at))

# Sends a message of the command history of all users (for moderators only)
@client.command()
async def history(ctx):
    if ctx.author.guild_permissions.administrator:
        
            hist = '\n'.join(command_history)
            histEmbed=discord.Embed(
                title='Command History',
                description=hist,
                color=discord.Colour.blue()
            )
            await ctx.send(embed=histEmbed)
    else:
        permEmbed=discord.Embed(
            title="You do not have permission to use this command!",
            description='',
            color=discord.Colour.blue()
        )
        await ctx.send(embed=permEmbed)

# Demographics command that outputs the number of users in each role and list the roles
@client.command()
async def demographics(ctx):
    # Get the list of roles
    roles = ctx.guild.roles
    # Get the list of members
    members = ctx.guild.members
    # Create a dictionary to store the role names and the number of members in each role
    role_dict = {}
    # Loop through each role
    for role in roles:
        # Get the number of members in the role
        role_count = len([member for member in members if role in member.roles])
        # Add the role name and count to the dictionary
        role_dict[role.name] = role_count
    # Sort the dictionary by the number of members in each role
    sorted_roles = sorted(role_dict.items(), key=lambda x: x[1], reverse=True)
    # Create a string to store the output
    output = ""
    # Loop through the sorted roles and add them to the output string
    for role in sorted_roles:
        output += f"{role[0]}: {role[1]}" + "\n"
    # Send the output string to the channel
    demEmbed = discord.Embed(
        title='Demographics\n',
        description=output,
        color=discord.Colour.blue()
    )
    await ctx.send(embed=demEmbed)
      
# Poll command that allows users to vote on a given question
@client.command()
async def poll(ctx, question, *options):
    # Send the poll message with the question and options
    
    message = (f"{question}\n\n" + "\n".join([f"{i}\u20e3 {option}" for i, option in enumerate(options, start=1)]))
    pollEmbed = discord.Embed(
        title="New Poll! Answer within 10 seconds.",
        description=message,
        color=discord.Colour.blue()
    )
    pollmsg = await ctx.send(embed=pollEmbed)
    # Add numbered reactions to the message for each option
    for i in range(1, len(options)+1):
        await pollmsg.add_reaction(f"{i}\u20e3")
    # Wait for the specified amount of time
    await asyncio.sleep(10)
    # Fetch the message again to get the updated reactions
    pollmsg = await pollmsg.channel.fetch_message(pollmsg.id)
    # Tally up the reactions and determine the winner
    winners = []
    max_count = 0
    for reaction in pollmsg.reactions:
        # Check if this reaction has the highest count
        if reaction.count > max_count:
            max_count = reaction.count
            winners = [reaction]
        # Check if this reaction has the same count as the current winners
        elif reaction.count == max_count:
            winners.append(reaction)
    if len(winners) == 1:
        # If there's only one winner, send a message with the winner
        winner = winners[0]
        await ctx.send(f"The winner is option {winner.emoji} with {winner.count-1} vote(s)!")
    else:
        # If there's a tie, send a message with the tied options
        tied_options = ", ".join([f"option {winner.emoji}" for winner in winners])
        await ctx.send(f"There is a tie between {tied_options} with {max_count-1} vote(s) each.")

# Spotify API Setup
SPOTIFY_CLIENT_ID = ""
SPOTIFY_CLIENT_SECRET = ""
SPOTIFY_PLAYLIST_ID = "37i9dQZEVXbLp5XoPON0wI"
# Verify the client ID and secret using the Spotipy import
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET))

# Recommend command that gets random song from spotify top songs
@client.command()
async def recommend(ctx):
    # Get a random track from the playlist
    playlist_tracks = sp.playlist_tracks(SPOTIFY_PLAYLIST_ID)['items']
    random_track = random.choice(playlist_tracks)['track']

    # Send the track information to the discord channel
    recs = discord.Embed(
        title="Check out this song:",
        description = f"{random_track['name']} by {random_track['artists'][0]['name']}",
        color=discord.Colour.blue()
    )
    await ctx.send(embed=recs)
    await ctx.send(f"{random_track['external_urls']['spotify']}")

# List of music trivia questions and answers
music_trivia = [
    {'question': 'Who is the lead singer of the band Nirvana?', 'answer': 'Kurt Cobain'},
    {'question': 'What is the best-selling album of all time?', 'answer': 'Thriller by Michael Jackson'},
    {'question': 'What is Freddie Mercury\'s real name?', 'answer': 'Farrokh Bulsara'},
    {'question': 'What is the name of the first EDM artist to win a Grammy?', 'answer': 'Skrillex'},
    {'question': 'What is the name of the first song ever played in space?', 'answer': 'Jingle Bells'},
    {'question': 'In The Big Lebowski, The Dude can\'t stand which band?', 'answer': 'The Eagles'},
    {'question': 'Who was the first woman ever inducted into the Rock and Roll Hall of Fame?', 'answer': 'Aretha Franklin'}
]

# Command to start a music trivia game
@client.command()
async def trivia(ctx):
    # Choose a random trivia question
    question = random.choice(music_trivia)

    # Send the question to the channel
    questionw = discord.Embed(
        title=(question['question']),
        color=discord.Colour.blue()
    )
    await ctx.send(embed=questionw)

    # Wait for an answer from the user
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    # Timeout exception if the user doesn't answer in time
    try:
        user_answer = await client.wait_for('message', timeout=10.0, check=check)
    except asyncio.TimeoutError:
        timeup = discord.Embed(
            title='Sorry, time is up!',
            color=discord.Colour.blue()
        )
        await ctx.send(embed=timeup)
        return

    # Check if the user's answer is correct and make it lowercase so it isn't case sensitive
    if user_answer.content.lower() == question['answer'].lower():
        correct = discord.Embed(
            title=(f'Congratulations, {ctx.author.name}! You got it right.'),
            color=discord.Colour.blue()
        )
        await ctx.reply(embed=correct)
    # If the answer is incorrect, send the correct answer
    else:
        wrong = discord.Embed(
            title=(f'Sorry, {ctx.author.name}, that is incorrect. The answer is {question["answer"]}.'),
            color=discord.Colour.blue()
        )
        await ctx.reply(embed=wrong)

genius = lyricsgenius.Genius("TMigSKQ5Y3Ck7Z9Ohr8ibIFun7RzQsgjr3EboExdEFt7jPWTO4HDCguhZlLKj-_V")

# Command to get lyrics for a song
@client.command()
async def lyrics(ctx, *, song):
    try:
        song = genius.search_song(song)
        songEmbed = discord.Embed(
            title=f"{song.title} by {song.artist}",
            description=f"{song.lyrics}",
            color=discord.Colour.blue()
        )
        await ctx.send(embed=songEmbed)
        #await ctx.send(f"**{song.title} by {song.artist}**\n{song.lyrics}")
    except:
        noSongEmbed = discord.Embed(
            title="Sorry, I couldn't find the lyrics for that song.",
            color=discord.Colour.blue()
        )
        await ctx.reply(embed=noSongEmbed)

# Mute command to mute users from typing and talking
@client.command()
async def mute(ctx, member : discord.Member, *, reason=None):
    if ctx.author.guild_permissions.administrator:
        guild = ctx.guild
        # finds the muted role
        mutedRole = discord.utils.get(guild.roles, name="Muted")
        # creates a muted role if there isn't one already
        if not mutedRole:
            mutedRole = await guild.create_role(name="Muted")
            for channel in guild.channels:
                await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=True)
        await member.add_roles(mutedRole, reason=reason)
        mutedEmbed=discord.Embed(
            title=f"Success: Muted user {member}!",
            color=discord.Colour.blue()
        )
        await ctx.send(embed=mutedEmbed)
        memberEmbed=discord.Embed(
            title=f"You have been muted in {guild} for {reason}!",
            color=discord.Colour.blue()
        )
        await member.send(embed=memberEmbed)
    else:
        permEmbed=discord.Embed(
            title="You do not have permission to use this command!",
            color=discord.Colour.blue()
        )
        await ctx.reply(embed=permEmbed)

    

# Unmute command to unmute muted users
@client.command()
async def unmute(ctx, member : discord.Member):
    if ctx.author.guild_permissions.administrator:
        guild=ctx.guild
        mutedRole = discord.utils.get(guild.roles, name="Muted")
        await member.remove_roles(mutedRole)
        unmutedEmbed=discord.Embed(
            title=f"Success: Unmuted user {member}!",
            color=discord.Colour.blue()
        )
        await ctx.send(embed=unmutedEmbed)

        DMEmbed=discord.Embed(
            title=f'You have been unmuted in {guild}!',
            color=discord.Colour.blue()
        )
        await member.send(embed=DMEmbed)

    else:

        permEmbed=discord.Embed(
            title="You do not have permission to use this command!",
            color=discord.Colour.blue()
        )
        await ctx.reply(embed=permEmbed)
    

client.run(token)