import cohere #import cohere for ai services
from rich import print#import rich for better print statements
from dotenv import dotenv_values#import dotenv to load environment variables

# Load environment variables
env_vars = dotenv_values(".env")
CohereAPIKey = env_vars.get("CohereAPIKey")# Load Cohere API key from environment variables

co = cohere.Client(api_key=CohereAPIKey)# Initialize Cohere client

# Define possible functions/commands
func = [
    "exit","general","realtime","open","close","play","generate image","system","content","google search","youtuber reminder","reminder"
]

# Initialize messages list
messages = []
# Define the preamble for the decision-making model
preamble = """
You are a very accurate Decision-Making Model, which decides what kind of a query is given to you.
You will decide whether a query is a 'general' query, a 'realtime' query, or is asking to perform any task or automation like 'open facebook, instagram', 'can you write a application and open it in notepad'
*** Do not answer any query, just decide what kind of query is given to you. ***
-> Respond with 'general ( query )' if a query can be answered by a llm model (conversational ai chatbot) and doesn't require any up to date information like if the query is 'who was akbar?' respond with 'general who was akbar?', if the query is 'how can i study more effectively?' respond with 'general how can i study more effectively?', if the query is 'can you help me with this math problem?' respond with 'general can you help me with this math problem?', if the query is 'Thanks, i really liked it.' respond with 'general thanks, i really liked it.' , if the query is 'what is python programming language?' respond with 'general what is python programming language?', etc. Respond with 'general (query)' if a query doesn't have a proper noun or is incomplete like if the query is 'who is he?' respond with 'general who is he?', if the query is 'what's his networth?' respond with 'general what's his networth?', if the query is 'tell me more about him.' respond with 'general tell me more about him.', and so on even if it require up-to-date information to answer. Respond with 'general (query)' if the query is asking about time, day, date, month, year, etc like if the query is 'what's the time?' respond with 'general what's the time?'.
-> Respond with 'realtime ( query )' if a query can not be answered by a llm model (because they don't have realtime data) and requires up to date information like if the query is 'who is indian prime minister' respond with 'realtime who is indian prime minister', if the query is 'tell me about facebook's recent update.' respond with 'realtime tell me about facebook's recent update.', if the query is 'tell me news about coronavirus.' respond with 'realtime tell me news about coronavirus.', etc and if the query is asking about any individual or thing like if the query is 'who is akshay kumar' respond with 'realtime who is akshay kumar', if the query is 'what is today's news?' respond with 'realtime what is today's news?', if the query is 'what is today's headline?' respond with 'realtime what is today's headline?', etc.
-> Respond with 'open (application name or website name)' if a query is asking to open any application like 'open facebook', 'open telegram', etc. but if the query is asking to open multiple applications, respond with 'open 1st application name, open 2nd application name' and so on.
-> Respond with 'close (application name)' if a query is asking to close any application like 'close notepad', 'close facebook', etc. but if the query is asking to close multiple applications or websites, respond with 'close 1st application name, close 2nd application name' and so on.
-> Respond with 'play (song name)' if a query is asking to play any song like 'play afsanay by ys', 'play let her go', etc. but if the query is asking to play multiple songs, respond with 'play 1st song name, play 2nd song name' and so on.
-> Respond with 'generate image (image prompt)' if a query is requesting to generate a image with given prompt like 'generate image of a lion', 'generate image of a cat', etc. but if the query is asking to generate multiple images, respond with 'generate image 1st image prompt, generate image 2nd image prompt' and so on.
-> Respond with 'reminder (datetime with message)' if a query is requesting to set a reminder like 'set a reminder at 9:00pm on 25th june for my business meeting.' respond with 'reminder 9:00pm 25th june business meeting'.
-> Respond with 'system (task name)' if a query is asking to mute, unmute, volume up, volume down , etc. but if the query is asking to do multiple tasks, respond with 'system 1st task, system 2nd task', etc.
-> Respond with 'content (topic)' if a query is asking to write any type of content like application, codes, emails or anything else about a specific topic but if the query is asking to write multiple types of content, respond with 'content 1st topic, content 2nd topic' and so on.
-> Respond with 'google search (topic)' if a query is asking to search a specific topic on google but if the query is asking to search multiple topics on google, respond with 'google search 1st topic, google search 2nd topic' and so on.
-> Respond with 'youtube search (topic)' if a query is asking to search a specific topic on youtube but if the query is asking to search multiple topics on youtube, respond with 'youtube search 1st topic, youtube search 2nd topic' and so on.
*** If the query is asking to perform multiple tasks like 'open facebook, telegram and close whatsapp' respond with 'open facebook, open telegram, close whatsapp' ***
*** If the user is saying goodbye or wants to end the conversation like 'bye jarvis.' respond with 'exit'.***
*** Respond with 'general (query)' if you can't decide the kind of query or if a query is asking to perform a task which is not mentioned above. ***
"""
# Define chat history for context
ChatHistory = [
    {"role":"User","message":"how are you"},
    {"role":"Chatbot","message":"general how are you"},
    {"role":"User","message":"do you like f1"},
    {"role":"Chatbot","message":"general do you like f1"},
    {"role":"User","message":"open chrome and tell me about max verstappen"},
    {"role":"Chatbot","message":"open chrome general tell me about max verstappen"},
    {"role":"User","message":"open chrome and brave"},
    {"role":"Chatbot","message":"open chrome, open brave"},
    {"role":"User","message":"what is todays date and by the way remind me that i have a meeting on 16th november at 5pm"},
    {"role":"Chatbot","message":"general what is today date, reminder 5:00pm 16th november meeting"},
    {"role":"User","message":"chat with me"},
    {"role":"Chatbot","message":"general chat with me"},
    
    
]

# Define the main function to interact with the decision-making model
def FirstLayerDMM(prompt: str = "test"):
    # Append the user prompt to messages
    messages.append({"role":"user","content":f"{prompt}"})


    # Create a streaming response from the Cohere API
    stream = co.chat_stream(
        model='command-r-plus',# Use the command-r-plus model
        message=prompt,# Set the user message
        temperature=0.7,# Set the temperature for response variability
        chat_history=ChatHistory,# Provide chat history for context
        prompt_truncation='OFF',# Disable prompt truncation
        connectors=[],# No additional connectors
        preamble=preamble# Set the preamble for the model 
    )
    # Initialize an empty response string
    response=""

    # Iterate through the streaming events
    for event in stream:
        if event.event_type=="text-generation":
            response += event.text# Append the generated text to the response

    
    # Clean and process the response
    response = response.replace("\n","")
    response = response.split(",")



    #strip whitespace from each task in the response
    response = [i.strip() for i in response]
    #filter response to only include valid functions/commands
    temp=[]
    #filter response to only include valid functions/commands
    for task in response:
        for f in func:
            if task.startswith(f):
                temp.append(task)#append valid task to temp

    #update response with filtered tasks
    response = temp
    #if response is empty, return a default message 
    if"(query)" in response:
        newresponse = FirstLayerDMM(prompt=prompt)
        return newresponse#recursively call the function if response is not valid
    else:
        return response#return the final response
    

# entry point for testing the function
if __name__=="__main__":
    #continuously prompt the user for input and display the model's response
    while True:
        print(FirstLayerDMM(input(">>> ")))#print the model's response