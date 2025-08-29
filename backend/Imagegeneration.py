import asyncio
from random import randint
from PIL import Image
import requests
from dotenv import get_key
import os
from time import sleep


#for opening and displaying images for given input
def open_images(prompt):
    folder_path = r"data"#folder where the data will be stored
    prompt = prompt.replace(" ", "_")#replace spaces with underscore

    #generating file names for the images
    Files = [f"{prompt}_{i}.jpg" for i in range(1, 5)]

    for jpg_file in Files:
        image_path = os.path.join(folder_path, jpg_file)
        try:
            #try to open and display the image
            img = Image.open(image_path)
            
            img.show()
            sleep(1)#wait for 1 sec in between showing images
        except IOError:
            print(f"Unable to open {image_path}")


#details for hugging face diffusion model
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {get_key('.env', 'HuggingFaceAPIKey')}"}


#async func to send the imput to hgging face api
async def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content


#async func to generate image
async def generate_image(prompt):
    tasks= []
    
    #create 5 images
    for _ in range(5):
        payload = {
            "inputs": f"{prompt}, quality=4K, sharpness=maximum, Ultra High details, high resolution, seed={randint(0, 1000000)}",
        }
        task = asyncio.create_task(query(payload))
        tasks.append(task)

    #waiting for all task to complete
    image_bytes_list = await asyncio.gather(*tasks)

    #saving the generated image to file
    for i, image_bytes in enumerate(image_bytes_list):
        with open(fr"data\{prompt.replace(' ', '_')}_{i+1}.jpg", "wb") as f:
            f.write(image_bytes)


#func to generate and open images
def GenerateImages(prompt: str):
    asyncio.run(generate_image(prompt))#executing async image generation
    open_images(prompt)#open the images


#monitoring the imgae generation
while True:

    try:
        #read the status and prompt from the data file
        with open(r"frontend\files\imagegeneration.data","r")as f:
            Data: str = f.read()


            Prompt, Status = Data.split(",")
            #checking image generation request
            if Status == "True":
                print("Generating Image.....")
                ImageStatus = GenerateImages(prompt=Prompt)

                #check the status again after generating the image
                with open(r"frontend\files\imagegeneration.data","w")as f:
                    f.write("False,False")#quit the loop
                    break

            else:
                sleep(1)#wait for 1 sec before checking again
            
    except:
        pass
