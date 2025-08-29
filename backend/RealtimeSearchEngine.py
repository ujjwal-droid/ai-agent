from googlesearch import search
from groq import Groq#import Groq for using Groq API
from json import load, dump#import load and dump for handling JSON files    
import datetime#import datetime for real-time information
from dotenv import dotenv_values#   import dotenv to load environment variables


# Load environment variables
env_vars = dotenv_values(".env")
# Load necessary environment variables
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

# Initialize Groq client
client = Groq(api_key=GroqAPIKey)

#define the system prompt for the chatbot
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***"""


#try to load existing chat log from a json file or create a new one if it doesn't exist
try:
    with open(r"data\Chatlog.json","r") as f:
        messages = load(f)
except:
    with open(r"data\Chatlog.json","w") as f:
        dump([], f)
    

# Function to perform a Google search and return formatted results
def GoogleSearch(query):
    results = list(search(query, advanced=True, num_results=5))
    Answer = f"The search results for '{query}' are:\n[start]\n"
    

    for i in results:
        Answer += f"Title: {i.title}\nDescription: {i.description}\n\n"

    Answer += "[end]"
    return Answer

#function to clean and modify the chatbot's answer
def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [ line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

#predefined conversation system message and an initial greeting
SystemChatBot = [
    {"role":"system", "content": System},
    {"role":"user", "content": "Hi"},
    {"role":"assistant", "content": "Hello! How can I assist you today?"}
    ]

# Function to get current date and time information
def Information():
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")
    
    data = f"Please use this real-time information if needed,\n"
    data +=f"Day: {day}\n"
    data +=f"Date:{date}\n"
    data +=f"Month:{month}\n"
    data +=f"Year: {year}\n"
    data += f"Time: {hour} hours :{minute} minutes :{second} seconds.\n"
    return data

#for handling the realtime search engine functionality
def RealtimeSearchEngine(prompt):
    global SystemChatBot , messages

    # Load existing chat log from a json file
    with open(r"data\Chatlog.json","r") as f:
        messages = load(f)
        messages.append({"role": "user" , "content": f"{prompt}"})
        
        # Append Google search results to the system messages
        SystemChatBot.append({"role": "system", "content": GoogleSearch(prompt)})

        #generate a response from the Groq API
        completion = client.chat.completions.create(
            model = "llama3-70b-8192",
            messages= SystemChatBot + [{"role": "system", "content": Information()}] + messages,
            max_tokens = 1024,
            temperature = 0.7,
            top_p=1,
            stream=True,
            stop =None
        )
        
        Answer = ""


        #join the response chunks from the streaming response
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content
        
        # Clean up the answer
        Answer = Answer.strip().replace("</s>", "")
        messages.append({"role": "assistant", "content": Answer})
        
        # Save the updated chat log back to the json file
        with open(r"data\Chatlog.json","w") as f:
            dump(messages, f, indent=4)

        #remove the last system message to avoid accumulation
        SystemChatBot.pop()
        return AnswerModifier(Answer=Answer)
    
#main input point for interaction
if __name__ == "__main__":
        while True:
            prompt = input("Enter your query:")
            print(RealtimeSearchEngine(prompt))              