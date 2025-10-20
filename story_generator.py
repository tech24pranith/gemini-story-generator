from dotenv import load_dotenv 
import os
from google import genai
from gtts import gTTS
from io import BytesIO


load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY") 
if not api_key:
    raise ValueError("API key not found")

client = genai.Client(api_key=api_key)


# Function --- images, style ---> story

def generate_story_from_images(images,style):
    # if not(1 <= len(images) <= 10):
    #     return "validation Error : please provide Images between 1 to 10"
    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[images,create_advanced_prompt(style)]

    )

    return response.text



def create_advanced_prompt(style):

    base_prompt = '''
                    ** Your persona : Friendly and Engaging storyteller 
                    ** Main goal : Tell the story in simple,clear and modern English
                    ** Your task : Create a story connecting all the uploaded images
                    ** Style of story : '{style}' genre
                    ** Use Indian names and characters
                    ** Make sure the flow of story goes by the order of images and every picture is related to each other 
                    
                    ** if the {style} == 'Comedy' . Make it very funny

                    *** OUTPUT FORMAT : ***

                        'Title' : Start with a simple and clear title 
                        ** Length : Minimum of 3 paras and Maximum of 4 paragraphs.  


    
                   '''
    
    # Advanced 

    style_instruction = ""

    if style=="Morale":
        style_instruction = "\n** Special Section : ** After the story , you must provide the morale in one liner using the exact tag 'MORALE:' that reveals the morale  "

    elif style=="Mystery":
        style_instruction = "\n** Special Section : ** After the story , you must provide the suspense in one line using the exact tag 'SUSPENSE:' that reveals the mystery "

    elif style == "Thriller":
        style_instruction = "\n** Special Section : ** After the story , you must provide a section where you need to provide the exact tag 'TWIST:' that reveals the twist "


    return base_prompt+style_instruction


# Func give story in text -----> audio

# gTTS library for speech ||||| Can also use TTS of gemini but a bit lengthy process 


def narrate_story(story_text):
    try:
        tts = gTTS(text=story_text, lang="en",slow=False)
        audio_fp = BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        return audio_fp
    
    except Exception as e:
        return f"Unexpected Error during API call : {e}"








