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
# Initialize an empty list to store chat messages
messages = []
# Define the system prompt for the chatbot
System = System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""
# Combine system prompt with chat history
SystemChatbot = [
    {"role":"system", "content": System}

]
# Load existing chat log from a json file
try:
    with open(r"data\Chatlog.json","r") as f:
        messages = load(f)# Load existing chat log from a json file
except (FileNotFoundError):
    # If file not found, create a new empty chat log
    with open(r"data\Chatlog.json","w") as f:
        dump([], f)

# Function to get current date and time information
def RealtimeInformation():
    current_date_time = datetime.datetime.now()# Get current date and time
    day = current_date_time.strftime("%A")# Get current day of the week
    date = current_date_time.strftime("%d")# Get current date of the month
    month = current_date_time.strftime("%B")# Get current month name
    year = current_date_time.strftime("%Y")# Get current year
    hour = current_date_time.strftime("%H")# Get current hour in 24-hour format
    minute = current_date_time.strftime("%M")# Get current minute
    second = current_date_time.strftime("%S")# Get current second


    # Format the date and time information into a string
    data = f"Please use this real-time information if needed,\n"
    data +=f"Day: {day}\nDate:{date}\nMonth:{month}\nYear: {year}\n"
    data += f"Time: {hour} hours :{minute} minutes :{second} seconds.\n"
    return data
# Function to clean and modify the chatbot's answer
def AnswerModifier(Answer):
    lines = Answer.split('\n')# Split the answer into lines
    non_empty_lines = [ line for line in lines if line.strip()]# Filter out empty lines
    modified_answer = '\n'.join(non_empty_lines)# Join non-empty lines back into a single string
    return modified_answer

# Main function to handle chatbot interactions
def Chatbot(Query):
    """Main function to handle chatbot interactions"""

    try:
        # load the chat log from a json file
        with open(r"data\Chatlog.json","r") as f:
            messages = load(f)

            # Append the user query to the messages list
            messages.append({"role": "user" , "content": f"{Query}"})

            # Create a streaming chat completion request to the Groq API
            completion = client.chat.completions.create(
                model = "llama3-70b-8192",# Specify the model to use
                messages=SystemChatbot +[{"role": "system", "content": RealtimeInformation()}] + messages,# Combine system prompt, real-time info, and chat history 
                max_tokens = 1024,# Set maximum tokens for the response
                temperature = 0.7,# Set temperature for response variability
                top_p=1,# Set top_p for nucleus sampling
                stream=True,# Enable streaming responses
                stop =None# No specific stop sequences
            )

            Answer= ""# Initialize an empty string to store the answer


            # Iterate through the streaming response chunks
            for chunk in completion:
                if chunk.choices[0].delta.content:# Check if the chunk contains content
                    Answer += chunk.choices[0].delta.content# Append the content to the answer

            Answer = Answer.replace("</s>", "")# Remove any end-of-sequence tokens from the answer

            # Append the assistant's answer to the messages list
            messages.append({"role": "assistant", "content": Answer})

            # Save the updated chat log back to the json file
            with open(r"data\Chatlog.json","w") as f:
                dump(messages, f, indent=4)

            # Modify and return the final answer
                return AnswerModifier(Answer=Answer)
            

    except Exception as e:
        # Handle exceptions and reset chat log if needed
        print(f"Error: {e}")
        with open(r"data\Chatlog.json","w") as f:
            dump([], f, indent=4)
        return Chatbot(Query)#recursively call the function in case of an error
        

if __name__=="__main__":
    while True:
        user_input = input("Enter Your Question:")#prompt the user for input
        print(Chatbot(user_input))#print the chatbot's response