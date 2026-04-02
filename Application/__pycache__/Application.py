#I previously was using the AppOpener library, but it seems the os library is closer to what we need

#I am unsure as to exactly where code like this should be in terms of the project. 
#I have made a new folder to hold the application I believe will be located on the users computer.
#This is a basic application that can open applications on the users computer
#Future goals will be to take info from the client on what to open and when

#Currently running the os library to open files 
#https://docs.python.org/3/library/os.html
import os

#Creates a txt file with the given text

def makeFile(input = "Example Text"):
    print("making file")
    with open('data.txt', 'w') as f:
        f.write(input)

makeFile()


#os.walk finds the directory path to a specific program, in our case it will be used to find spotify 
#to then open
#https://stackoverflow.com/questions/65501760/startfile-filepath-should-be-string-bytes-or-os-pathlike-not-list

def find_files(filename, search_path):  
   print("finding file")  
   for root, dir, files in os.walk(search_path, topdown=True):
      if filename in files:
         print("Found File!")
         return os.path.join(root, filename)
      else:
          print("File not found")

#searches alot of files
def startSpotify():
    find = find_files("Spotify.exe",r"C:\Users")
    os.startfile(find)


#def find(name, path):
    #for root, dirs, files in os.walk(path):
        #if name in files:
            #return os.path.join(root, name)
        

#Opens the given file on a native text editor
#The doccumentation mentioned the os.startfile command may run into trouble with other
#operating systems. If you can you run it and let me know if you get an error on your machine
def startFile():
    print("opening file")
    os.startfile("data.txt")
    #os.startfile(r'C:\Users\winde\AppData\Roaming\Spotify\Spotify.exe')
    
    
    #This is the code to open spotify with the os library given my specific path.
    #The application closes as soon as the program is completed. This file doesnt do anything else so it closes instantly, but if
    #it were running through the client, it would close once the client is shut off
    #This can be seen with the current setup with the data.txt file which stays open
    #os.startfile(r'C:\Users\winde\AppData\Roaming\Spotify\Spotify.exe')


#startFile()

#This file is currently set up to be the bare minimum it needs to connect to the client and run
#Things it needs in the future:
#Keep file open
#Fail checks
#Taking a string that is written in a file
#integration with spotify api


