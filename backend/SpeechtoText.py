from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import os   
import mtranslate as mt

#load environent variables from .env file
env_vars = dotenv_values(".env")

#get language setting from .env
InputLanguage = env_vars.get("InputLanguage")

#for speech recognition process
HtmlCode = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {
            recognition = new webkitSpeechRecognition() || new SpeechRecognition();
            recognition.lang = '';
            recognition.continuous = true;

            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript;
            };

            recognition.onend = function() {
                recognition.start();
            };
            recognition.start();
        }

        function stopRecognition() {
            recognition.stop();
            output.innerHTML = "";
        }
    </script>
</body>
</html>'''

# replace the language setting in the html code with the input language from environmental variables
HtmlCode = str(HtmlCode).replace("recognition.lang = '';", f"recognition.lang = '{InputLanguage}';")


#write the modified code to a file
with open(r"data\Voice.html", "w") as f:
    f.write(HtmlCode)

#get the current directory
current_dir = os.getcwd()
#for generating file path for html file
Link = f"{current_dir}/data/Voice.html"

#setting chrome options for webdriver
chrome_options = Options()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")
chrome_options.add_argument("--headless=new")


#initializing the chrome webdriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

#defining the pathe for temp files
TempDirPath = rf"{current_dir}frontend/files"

#setting the assistant status
def SetAssistantStatus(Status):
    with open(rf"{TempDirPath}/Status.data", "w", encoding = "utf-8") as file:
        file.write(Status)

#functions to modify a query in order to ensure proper formatting
def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words= new_query.split()
    question_words = ["what", "when", "how", "why", "where", "which", "who", "whom", "whose","can you","what's","what's","where's","how's","can you"]

    # checking if the query is a question and add a question mark to it
    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] in [',',"?",'!']:
            new_query = new_query[:-1] + "?"
        
        else:
            new_query += "?"

    else:
        #add a period if the input is not the question
        if query_words[-1][-1] in ['.', '!', '?']:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."


    return new_query.capitalize()

#for translating english to text usin mtranslate
def UniversalTranslate(Text):
    english_translation = mt.translate(Text, "en", "auto")
    return english_translation.capitalize()


def SpeechRecognition():

    #opens he file in the browser
    driver.get("file:///" + Link)
    #start speech recognition by clicking the start button
    driver.find_element(by= By.ID, value ="start").click()


    while True:
        try:
            #get the recognised text
            Text = driver.find_element(by= By.ID, value ="output").text

            if Text:
                #stop the function by clicking stop button
                driver.find_element(by= By.ID, value ="end").click()
                
                #if input language is english return modified query
                if InputLanguage.lower() == "en" or "en" in InputLanguage.lower():
                    return QueryModifier(Text)
                
                else:
                    #if the input language is not english then translate the text and return it
                    SetAssistantStatus("Translating....")
                    return QueryModifier(UniversalTranslate(Text))
                
        except Exception as e:
            pass

#main execution block
if __name__ == "__main__":
    while True:

        #continuously perform the speech recognition
        Text = SpeechRecognition()
        print(Text)

        