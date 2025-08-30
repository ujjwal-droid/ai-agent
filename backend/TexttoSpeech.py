import pygame #for handling audio playback
import random #for generating random choices
import asyncio #for asynchronous operations
import edge_tts #for text to speech functionality
import os #for file path handling
from dotenv import dotenv_values #for reading environment variables

#to load environment variables  
env_vars = dotenv_values(".env")
AssistantVoice = env_vars.get("AssistantVoice",)#get the voice from .env


#for converting text to audio file
async def TextToAudioFile(text) -> None:
    file_path = r"data\speech.mp3"#path to save the speech file
    
    if os.path.exists(file_path):#check if the file already exist
        os.remove(file_path)#remove it if exist inorder to avoid overwriting

    #communicate object to generate speech
    communicate = edge_tts.Communicate(text, AssistantVoice,pitch ="+5Hz",rate="+13%")
    await communicate.save(r"data\speech.mp3")#saving the speech as mp3 file

#for manafing TTS functionality
def TTS(Text , func=lambda r=None: True):
    while True:
        try:
            #converting text to an audio simultaneously
            asyncio.run(TextToAudioFile(Text))

            #initialize pygame mixer for audio playback
            pygame.mixer.init()
            
            #load the generated speech file
            pygame.mixer.music.load(r"data\speech.mp3")
            pygame.mixer.music.play()

            #loopig it until audio is finished or the function stops
            while pygame.mixer.music.get_busy():
                if func() == False:#check if the external function return false
                    break
                pygame.time.Clock().tick(10)# limiting loop to 10 ticks

            return True#true for successfull execution
        
        except Exception as e:#handling exceptions during execution
            print(f"Error in TTS: {e}")

        finally:
            try:
                #call the provided function with false to signal end of TTS

                func(False)
                pygame.mixer.music.stop()#stop the audio playback
                pygame.mixer.quit()#exit the pygame mixer

            except Exception as e:#handling any exception during the wrapup
                print(f"Error in finally block: {e}")

#for mananging long text with additional responses
def TextToSpeech(Text,func=lambda r=None: True):
    Data = str(Text).split(".")
    
    
    #list of predefined responses
    responses = [
        "The rest of the result has been printed to the chat screen, kindly check it out sir.",
        "The rest of the text is now on the chat screen, sir, please check it.",
        "You can see the rest of the text on the chat screen, sir.",
        "The remaining part of the text is now on the chat screen, sir.",
        "Sir, you'll find more text on the chat screen for you to see.",
        "The rest of the answer is now on the chat screen, sir.",
        "Sir, please look at the chat screen, the rest of the answer is there.",
        "You'll find the complete answer on the chat screen, sir.",
        "The next part of the text is on the chat screen, sir.",
        "Sir, please check the chat screen for more information.",
        "There's more text on the chat screen for you, sir.",
        "Sir, take a look at the chat screen for additional text.",
        "You'll find more to read on the chat screen, sir.",
        "Sir, check the chat screen for the rest of the text.",
        "The chat screen has the rest of the text, sir.",
        "There's more to see on the chat screen, sir, please look.",
        "Sir, the chat screen holds the continuation of the text.",
        "You'll find the complete answer on the chat screen, kindly check it out sir.",
        "Please review the chat screen for the rest of the text, sir.",
        "Sir, look at the chat screen for the complete answer."
    ]

    #if the text is longer than 4 lines and 250 words
    if len(Data) > 4 and len(Text) >= 100000:
        TTS(" ".join(Text.split(".")[0:2])+". "+ random.choice(responses) , func)
    
    #otherwise play the whole text

    else:
        TTS(Text, func)


#main execution loop
if __name__ == "__main__":
    while True:
        TextToSpeech(input("Enter the text: "))#prompting user for input

            

