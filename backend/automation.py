from AppOpener import close, open as appopen #functions for opening and closing apps
from webbrowser import open as webopen #functions for opening links in browser
from pywhatkit import playonyt,search #functions for playing youtube videos and searching on google
from dotenv import dotenv_values # for loading environment variables from .env file
from bs4 import BeautifulSoup # for parsing HTML content
from rich import print #for pretty printing
from groq import Groq #Groq API client
import webbrowser# for opening web pages
import requests# for making HTTP requests
import subprocess# for running system commands
import keyboard# for simulating keyboard events
import asyncio# for asynchronous programming
import os# for interacting with the operating system

# Load environment variables
env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")#retrieve Groq API key

# define CSS classes for web scraping
classes = [ ["zCubwf", "hgKElc", "LTKOO SY7ric", "Z0LcW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee", "tw-Data-text tw-text-small tw-ta", "IZ6rdc", "05uR6d LTKOO", "vlzY6d", "webanswers-webanswers_table_webanswers-table", "dDoNo ikb4Bb gsrt", "sXLa0e", "LWkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]]
# set a user agent for HTTP requests
useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

# initialize Groq API client
client = Groq(api_key=GroqAPIKey)

# define some professional responses
professional_response = [
    "Ensuring your satisfaction is my top priority. Should you require any additional assistance, feel free to let me know.",
    "I remain at your service for any further questions or assistance. Please do not hesitate to reach out."

]

# initialize an empty list to store conversation messages
messages = []

# define system message for chatbot
SystemChatBot = [{"role": "system", "content": f"Hello, I am {os.environ['Username']}, You're a content writer. You have to write content like letter, stories, research papers, blogs, essays, poems, quotes, etc."}]

# function to perform a Google search
def GoogleSearch(Topic):
    search(Topic)#uses pywhatkit's search function to perform a google search
    return True#indicates successful execution

# function to generate content using AI
def content(Topic):
    # nested function to open a file in Notepad
    def OpenNotepad(File):
        default_text_editor="notepad.exe"
        subprocess.Popen([default_text_editor, File])
    # nested function to generate content using Groq API
    def ContentWriteAI(prompt):
        messages.append({"role": "user", "content": f"{prompt}"})#append user prompt to messages list


        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",#model name
            messages= SystemChatBot + messages,#system and user messages
            max_tokens=2048,#maximum tokens in response
            temperature=0.7,#creativity level
            top_p=1,#nucleus sampling for diversity
            stream=True,#streaming response
            stop=None,#no specific stop sequences
        )


        Answer = ""#initialize empty string for AI response

        # concatenate streamed response chunks
        for chunk in completion:#iterate through streamed response
            if chunk.choices[0].delta.get("content"):#check if content exists in chunk
                Answer += chunk.choices[0].delta.content



        Answer = Answer.replace("</s>", "")#clean up response by removing unwanted tokens
        messages.append({"role": "assistant", "content": Answer})#append AI response to messages list
        return Answer

    
    Topic: str = Topic.replace("Content ", "")#clean up topic string
    ContentByAI = ContentWriteAI(Topic)       #generate content using AI


    # create data directory if it doesn't exist
    with open("data\{Topic.lower().replace(' ', '')}.txt", "w", encoding="utf-8") as file:#open file to write content
        file.write(ContentByAI)#write AI-generated content to file
        file.close()#close file


#for searching a topic on youtube
def YouTubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}"#construct youtube search URL
    webbrowser.open(Url4Search)#open URL in web browser
    return True#indicates successful execution

#for playing a youtube video
def PlayYouTube(Topic):#uses pywhatkit's playonyt function to play a youtube video based on the given topic
    playonyt(Topic)#plays the first video result on youtube
    return True#indicates successful execution
PlayYouTube("https://www.youtube.com/watch?v=c7JhqqByKg4&pp=0gcJCbIJAYcqIYzv")
#for opening an app or a relevant website
def OpenApp(app, sess=requests.session()):
    try:
        appopen(app, match_closest=True, output = True, throw_error=True)#tries to open the app using AppOpener
        return True#indicates successful execution
    

    except:
        # if app opening fails, it tries to search for the app online and open the first relevant link
        def extract_links(html):
            if html is None:
                return []
            
            soup = BeautifulSoup(html, 'html.parser')#parse HTML content
            links = soup.find_all('a',{'jsname': 'UWckNb'})#find all anchor tags with specific attribute
            return [link.get('href') for link in links]#extract href attributes from anchor tags
        

        # nested function to perform a Google search
        def search_google(query):
            url=f"https://www.google.com/search?q={query}"#construct google search URL
            headers={'User-Agent': useragent}#set user agent for request
            response=sess.get(url,headers=headers)#make GET request to google search URL

            if response.status_code==200:
                return response.text#return HTML content if request is successful
            else:
                print("Failed to retieve search results")#print error message
                return None

        html = search_google(app)#perform google search for the app name


        if html:
            link = extract_links(html)[0]#extract first relevant link from search results
            webopen(link)#open the link in web browser

        return True#indicates successful execution

def CloseApp(app):
    if "chrome" in app:
        pass#to be implemented later
    else:
        try:
            close(app, match_closest=True, output = True, throw_error=True)#tries to close the app using AppOpener
            return True# indicates successful execution
        except:
            return False#indicates failure to close app
#for system commands like volume control        
def System(command):
    # nested function to mute system volume
    def mute():
        keyboard.press_and_release("volume mute")
    # nested function to unmute system volume   
    def unmute():
        keyboard.press_and_release("volume unmute")
    # nested function to increase system volume
    def volumeup():
        keyboard.press_and_release("volume up")
    #  nested function to decrease system volume
    def volumedown():
        keyboard.press_and_release("volume down")

    # execute appropriate system command based on input
    if command == "mute":
        mute()
    
    elif command == "unmute":
        unmute()

    elif command == "volume up":
        volumeup()
    
    elif command == "volume down":
        volumedown()
    
    return True#indicates successful execution

# asynchronous function to translate and execute commands
async def TranslateAndExecute(commands: list[str]):

    funcs = []#list to store asynchronous tasks

    for command in commands:

        if command.startswith("open "):#for opening apps or websites
            
            
            if "open it" in command:#ignore open it commands
                pass

            if"open file" == command:#ignore open file commands
                pass

            else:
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open "))#create asynchronous task to open app or website
                funcs.append(fun) 

        elif command.startswith("general"): #placeholder for general commands
            pass

        elif command.startswith("realtime"):#placeholder for realtime commands
            pass

        elif command.startswith("close "):#for closing apps
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close "))#create asynchronous task to close app
            funcs.append(fun)

        elif command.startswith("play"):#for playing youtube videos
            fun = asyncio.to_thread(PlayYouTube, command.removeprefix("play "))#create asynchronous task to play youtube video
            funcs.append(fun)

        elif command.startswith("content"):#for generating content using AI
            fun = asyncio.to_thread(content, command.removeprefix("content "))#create asynchronous task to generate content
            funcs.append(fun)

        elif command.startswith("google search"):#for performing google searches
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search "))#create asynchronous task to perform google search
            funcs.append(fun)
        
        elif command.startswith("youtube search"):#for performing youtube searches
            fun = asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search "))#create asynchronous task to perform youtube search
            funcs.append(fun)

        elif command.startswith("system"):#for executing system commands
            fun = asyncio.to_thread(System, command.removeprefix("system "))#create asynchronous task to execute system command
            funcs.append(fun)


        else:
            print(f"Npfunction found for command: {command}")#print error message for unrecognized command

    
    results = await asyncio.gather(*funcs)#gather results of all asynchronous tasks


    for result in results:#yield results one by one
        if isinstance(result, str):
            yield result
        else:
            yield result


# main asynchronous function to automate command execution
async def Automation(commands: list[str]):
    async for result in TranslateAndExecute(commands):#iterate through results of command execution
        pass

    return True






