# Make sure server is running before running the Client/Bot

import socket
import os
import PySimpleGUI as sg
ServerIP = "170.187.157.166"
# Switch to below if you want to run locally
# ServerIP = socket.gethostbyname(socket.gethostname())

ServerPort = 12001
ADDRESS = (ServerIP, ServerPort)

# Very simple UI build by looking at this tutorial https://thenewstack.io/python-for-beginners-how-to-build-a-gui-application/
#Import PySimpleGUI
import PySimpleGUI as sg
 
#Draw the button
layout = [[sg.Text('Hello! Thanks for downloading PolyMusic Bot and its companion app.')],
          [sg.Text('Which music service would you like to listen with?')],
          [sg.Text('After you have chosen and saved, close this window to begin playing music with your friends from Discord!')],
          [sg.Radio('Spotify', "RADIO1", default=True, key="spotify")],
          [sg.Radio('Apple Music', "RADIO1", default=False, key="applemusic")],
          [sg.Radio('iTunes', "RADIO1", default=False, key="iTunes")],
          [[sg.Text("Choose a file: "), sg.Input(key="path"), sg.FileBrowse()]],
          [sg.Button('Save',size=(20,2))]]
musicType = "spotify"
musicPath = ""      
sg.theme("DarkTeal2")
#Draw the window
window = sg.Window('PolyMusicBot', layout, size=(600,300))
 
while(True):
    #Define what happens when the button is clicked
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    if event == "Save":
        if values["spotify"] == True: musicType = "spotify"
        if values["applemusic"] == True: musicType = "applemusic"
        if values["iTunes"] == True: musicType = "iTunes"
        musicPath = values[r'path']

#This is a leftover from a previous method of finding spotify. With our current method it is no longer necessary

#def find_files(filename, search_path):  
     #print("finding file")  
     #for root, dir, files in os.walk(search_path, topdown=True):
      #if filename in files:
         #print("Found File!")
         #print(os.path.join(root, filename))
         #print(os.path(filename))
         #return os.path.join(root, filename)
      #else:
          #print("File not found")
          #return(r"C:\Users")

#searches to the specified path  of files  
def startFile():
        
        #This opens the text file with the message
        print("making file")
        with open('data.txt', 'w') as f:
            f.write(str(message.decode()))
        print("opening file")
        os.startfile('data.txt')
        
        #Here is where we use musicType to determine how you would deal with the received data
        print(musicPath)
        #find = find_files("Spotify.exe",musicPath)
        os.startfile(musicPath)  
        print("opening file")
        os.startfile("data.txt")



# Create Client Socket
try:
    ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as err:
    print (f'Unable to create socket {err}\n')

# Establish connection with the server
try:
    ClientSocket.connect((ADDRESS))
    print ('Client connected to the server')
    while(True):
        print(musicPath)
        
        # Recieve the message from the server
        message = ClientSocket.recv(1024)
        # Print message to terminal
        print (f'Response From Server:  {str(message.decode())}')

        # Close the connection if the server has closed the connection
        if not message:
            break

        print("starting file")
        startFile()

       

    #os.walk finds the directory path to a specific program, in our case it will be used to find spotify 
    #to then open
    #https://stackoverflow.com/questions/65501760/startfile-filepath-should-be-string-bytes-or-os-pathlike-not-list

    

        #Create a condition for closing the connection here if needed
        # if condition:
        #     break
except socket.error as err:
    print (f'Unable to connect to the server {err}')

# Close the connection
ClientSocket.close()