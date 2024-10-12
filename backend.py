import os
import time

from dotenv import load_dotenv
from google.api_core.exceptions import ResourceExhausted, InternalServerError
import google.generativeai as genai
# from PIL import Image, ImageGrab
#import pygetwindow as gw

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-pro-002')
retries = 0

# Create Gemini model
model = genai.GenerativeModel(
    model_name = "gemini-1.5-pro-002",
    system_instruction = f"""
        You are a language expert and tutor who finds joy in teaching others and assisting users in learning differnet languages.
        Your main objective is to teach another language to a user, providing a similar experience as Duolingo."""
        
    )

chat = model.start_chat(history=[], enable_automatic_function_calling=False) # start model chat history

# translate
def caption_capture(language: str, image) -> str:
    """Look at current window once and only once, output a single verbal response or type out a response. This function can also look at what's currently on screen and remember information from this screen This function is not capable of taking any other actions.
        
    Args:
    
        image: full image screenshot, will be cropped within the backend program
    """
    global retries # the api sometimes dies, so retry if necessary - up to 3 retries

    if retries == 3:
        retries = 0
        print('An unexpected error occurred on Google\'s side.	Wait a bit and retry your request. If the issue persists after retrying, please report it using the Send feedback button in Google AI Studio.')        
        return
    
    # image = ImageGrab.grab(bbox=(gw.getActiveWindow().left, gw.getActiveWindow().top, gw.getActiveWindow().left+gw.getActiveWindow().width, gw.getActiveWindow().top+gw.getActiveWindow().height))
    
    model_prompt = f"""
        ### Instructions

        You are given an image of a chrome screen. Somewhere on this screen is a video playing. Based on this screenshot of the video:
            1. Identify where the video is.
            2. Identify what is going on in the video and silently analyze in depth the characters and setting of the scene.
            3. Now focus on the subtitles of the video. The subtitles within the video are most likely located at the bottom of the video, but it is possible that it is somewhere else. Find the subtitles, and output the subtitles in its original language. Use optical character recognition, do not interpret anything. Output the subtitles EXACTLY as shown.
            4. Now taking this text that you extracted, translate it into {language}, maintaining the SAME gramatical structure and nuances as the original text.
            5. After you have both the original text and the translated text, do the following:
                a. Split up the original sentence by word/phrase if applicable.
                b. For each word/phrase, print the original word in its original language followed by a dash (-), and followed by the translation of the original word/phrase in {language}
                c. After repeating step b for every word, ONLY IF NECESSARY, begin explaining the nuances of the reltaionships between words. An example of this would be in Mandarin, where two words next to each other changes the meaning of one or another. Keep this in mind as well when giving direct translations for each word.
                If there is no hidden meaning or nuances, then do NOT elaborate, and skip step c. For example, if the translation is direct and accurate, do NOT analyze anything.
                
        ### Output Format
        Original Text:
        <original text>

        Translated Text:
        <translated text>

        Phrase Breakdown:
        <word/phrase 1> - <translated word/phrase 1>
        <word/phrase 2> - <translated word/phrase 2>
        <word/phrase 3> - <translated word/phrase 3>
        ...
        <word/phrase n> - <translated word/phrase n>
                
        Additional Analysis: (skip this analysis if not necessary, otherwise output this)
        <analysis of nuance 1>
        <analysis of nuance 2>
        ...
        <analysis of nuance n>
        """

    try:
        #response = chat.send_message([image, model_prompt])
        response = chat.send_message([image, model_prompt])
        function_calls = 0

        for part in response.parts:
            if fn := part.function_call:
                if callable(globals().get(fn.name)):
                    try:
                        func = globals()[fn.name]
                        print(f'Function Called: {fn.name}')
                        kwargs = fn.args
                        func(**kwargs)
                        function_calls += 1
                        retries = 0
                    except Exception as e:
                        print('Unexpected error encountered attempting to open function... Trying again...')
                        print(f'Error Message:\n{e}')
                        caption_capture(model_prompt) 

        if function_calls == 0:
            retries += 1
            print('retrying...')
            caption_capture(model_prompt)  #if model only generates text instead of calling function, retry

    except ResourceExhausted as resource_error:
        print(f'You have exceeded the API call rate. Please wait a minute before trying again... \nError message from Google:\n{resource_error}')
    except InternalServerError as internal_error:
        retries += 1
        time.sleep(1)
        print(f'An expected error occured on Google\'s side. Retrying after 1 second cooldown... Attempt {retries}/3')
        print(f'Error message from Google:\n{internal_error}')
        caption_capture(model_prompt)
    except Exception as e:
        print(f'Unknown error encountered. \nError message from Google:\n{e}')


def test(language: str, input: str) -> str:
    
    model_prompt = f"""
        ### Instructions

        You are given an image of a chrome screen. Somewhere on this screen is a video playing. Based on this screenshot of the video:
            1. Identify where the video is.
            2. Identify what is going on in the video and silently analyze in depth the characters and setting of the scene.
            3. Now focus on the subtitles of the video. The subtitles within the video are most likely located at the bottom of the video, but it is possible that it is somewhere else. Find the subtitles, and output the subtitles in its original language. Use optical character recognition, do not interpret anything. Output the subtitles EXACTLY as shown.
            4. Now taking this text that you extracted, translate it into {language}, maintaining the SAME gramatical structure and nuances as the original text.
            5. After you have both the original text and the translated text, do the following:
                a. Split up the original sentence by word/phrase if applicable.
                b. For each word/phrase, print the original word in its original language followed by a dash (-), and followed by the translation of the original word/phrase in {language}
                c. After repeating step b for every word, ONLY IF NECESSARY, begin explaining the nuances of the reltaionships between words. An example of this would be in Mandarin, where two words next to each other changes the meaning of one or another. Keep this in mind as well when giving direct translations for each word.
                If there is no hidden meaning or nuances, then do NOT elaborate, and skip step c. For example, if the translation is direct and accurate, do NOT analyze anything.
                
        ### Output Format
        Original Text:
        <original text>

        Translated Text:
        <translated text>

        Phrase Breakdown:
        <word/phrase 1> - <translated word/phrase 1>
        <word/phrase 2> - <translated word/phrase 2>
        <word/phrase 3> - <translated word/phrase 3>
        ...
        <word/phrase n> - <translated word/phrase n>
                
        Additional Analysis: (skip this analysis if not necessary, otherwise output this)
        <analysis of nuance 1>
        <analysis of nuance 2>
        ...
        <analysis of nuance n>
        """

    try:
        #response = chat.send_message([image, model_prompt])
        response = chat.send_message([input, model_prompt])
        function_calls = 0

        for part in response.parts:
            if fn := part.function_call:
                if callable(globals().get(fn.name)):
                    try:
                        func = globals()[fn.name]
                        print(f'Function Called: {fn.name}')
                        kwargs = fn.args
                        func(**kwargs)
                        function_calls += 1
                        retries = 0
                    except Exception as e:
                        print('Unexpected error encountered attempting to open function... Trying again...')
                        print(f'Error Message:\n{e}')
                        caption_capture(model_prompt) 

        if function_calls == 0:
            retries += 1
            print('retrying...')
            caption_capture(model_prompt)  #if model only generates text instead of calling function, retry

    except ResourceExhausted as resource_error:
        print(f'You have exceeded the API call rate. Please wait a minute before trying again... \nError message from Google:\n{resource_error}')
    except InternalServerError as internal_error:
        retries += 1
        time.sleep(1)
        print(f'An expected error occured on Google\'s side. Retrying after 1 second cooldown... Attempt {retries}/3')
        print(f'Error message from Google:\n{internal_error}')
        caption_capture(model_prompt)
    except Exception as e:
        print(f'Unknown error encountered. \nError message from Google:\n{e}')

test('english', 'hola, como estas?')
