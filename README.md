# DiscordMusicBot
This is a private repository to host the Team 15 Project. Our documentation (Design Document) can also be found here.

## Directions on how to start the website locally (Online it is here: https://bot.shiftsmart.me/ )
1. Navigate to the website directory inside the DiscordMusicBot folder
1. Install node from here: https://nodejs.org/en/download
2. Install express here: https://expressjs.com/en/starter/installing.html (or do 'npm install express' in the terminal)
3. Run 'node index.js' in your terminal in the website directory (/DiscordMusicBot/website/)
4. Go to your local host IP to access it. http://localhost:3000 
4. Login with Discord and add the bot to your server

Note: You can only add the bot to Discord through the local host by running 'node index.js' in the website directory.

## Directions on how to start the bot locally (Online it is already hosted 24/7 on our server. If you run it locally, you may get two responses from the same command.)
1. Install Discord.py here: https://discordpy.readthedocs.io/en/stable/intro.html#installing
2. Install spotipy here: https://spotipy.readthedocs.io/en/2.22.1/ (You can just use 'pip install spotipy --upgrade')
3. Install lyricgenius here: https://lyricsgenius.readthedocs.io/en/master/ (You can just use 'pip install lyricsgenius')
4. Add the d_token.txt file into the bot directory (/DiscordMusicBot/bot/) that only contains the Discord token provided in the Canvas *submission*
5. On line 274 and 275 in MainBot.py, add the Spotify Client ID and the Spotify Client Secret ID tokens provided in the Canvas *submission comments*
6. Run MainBot.py from the Bot directory (/DiscordMusicBot/bot/) by running just the Python file

Note: The '!lyrics [song]' command only works with the locally hosted bot by running MainBot.py in the bot directory.

## Directions on how to run the client application locally:
1. Make sure the ServerIP address in Server.py is set to socket.gethostbyname(socket.gethostname()) rather than the IP address of our server
2. Run Server.py in the Server folder. This connects to the discord bot if it is running and serves data to the client application when certain commands are called.
3. Install python simple GUI here: https://pypi.org/project/PySimpleGUI/  (I just used pip install PySimpleGUI) (This is used to generate the GUI for the client application)
4. Comment out line 6 and uncomment line 8 in Client.py to make sure the client connects to the local host
5. Run Client.py located in the Client folder
