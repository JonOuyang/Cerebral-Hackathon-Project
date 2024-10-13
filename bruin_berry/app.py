import os
import time
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.utils import secure_filename
from PIL import Image, ImageGrab
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted, InternalServerError
import pygetwindow as gw

app = Flask(__name__)
CORS(app) 

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

chat = genai.GenerativeModel(
    model_name="gemini-1.5-flash-002",
    system_instruction=(
        "You are a language expert translating text from images."
    )
).start_chat(history=[], enable_automatic_function_calling=False)


@app.route('/upload-image', methods=['FETCH'])
def translation():
    # if 'image' not in request.files:
    #     return jsonify({'error': 'No image uploaded.'}), 400

    # image = request.files['image']
    # if image.filename == '':
    #     return jsonify({'error': 'No selected file.'}), 400


    # filename = secure_filename(image.filename)
    # image_path = os.path.join('uploads', filename)
    # os.makedirs('uploads', exist_ok=True)
    # image.save(image_path)
    
    image_path = ImageGrab.grab(bbox=(gw.getActiveWindow().left, gw.getActiveWindow().top, gw.getActiveWindow().left+gw.getActiveWindow().width, gw.getActiveWindow().top+gw.getActiveWindow().height))


    response_text = caption_capture('english', image_path)


    return jsonify({'result': response_text})


def caption_capture(language, image_path, retries=0):
    if retries >= 3:
        return (
            "An unexpected error occurred. Please try again later."
        )

    try:

        with Image.open(image_path) as img:

            model_prompt = f"""
            ### Instructions

            You are given an image of a chrome screen. Analyze this video and look for mediums of interest. We classify mediums of interest as (youtube) videos, netflix videos, manga panels, and anything else that a user would most likely be primarily paying attention to:
                1. Identify where the medium is. You will ONLY be focusing on this medium, ignore all other distractions. Identify and reason (silently) what the user is most likely paying attention to based off of what the page is (i.e. Youtube - youtube videos or Netflix - netflix video)
                2. Identify what is going on in the video or image and silently analyze in depth the characters and setting of the scene.
                3. Now focus on the subtitles or text of the video or image. The subtitles within the video are most likely located at the bottom of the video, but it is possible that it is somewhere else. Find the subtitles, and output the subtitles in its original language. Use optical character recognition, do not interpret anything. Output the subtitles EXACTLY as shown. Follow the same instructions for textual mediums like manga
                4. Now taking this text that you extracted, translate it into {language}, maintaining the SAME gramatical structure and nuances as the original text.
                5. After you have both the original text and the translated text, do the following:
                    a. Split up the original sentence by word/phrase if applicable.
                    b. For each word/phrase, print the original word in its original language followed by a dash (-), and followed by the translation of the original word/phrase in {language}. Grammatical punctuation should be appended to the end of a word/phrase and NOT separated -- do NOT analyze them unless they gave the original word a different meaning. This includes but is not limited to question marks (?), explamation points (!), periods(.), etc
                    c. After repeating step b for every word, ONLY IF NECESSARY, begin explaining the nuances of the reltaionships between words. An example of this would be in Mandarin, where two words next to each other changes the meaning of one or another. Keep this in mind as well when giving direct translations for each word.
                    If there is no hidden meaning or nuances, then do NOT elaborate, and skip step c. For example, if the translation is direct and accurate, do NOT analyze anything.
                    
            When responding, omit all greetings and farewells. You are already well aquainted with the user, so
            - do NOT ask the user any questions
            - do NOT greet the user
            - do NOT say "thank you" or any sort of "youre welcome"
            - do NOT ask the user if they have any questions
            - do NOT tell the user anything that is not related to the language translation, including but not limited to "let me know if you have any other questions"
            
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


            response = chat.send_message([img, model_prompt])
            return response.text

    except (ResourceExhausted, InternalServerError) as e:
        print(f"Error: {e}. Retrying...")
        time.sleep(1)
        return caption_capture(language, image_path, retries + 1)

    except Exception as e:
        print(f"Unexpected error: {e}")
        return "An error occurred during translation."
    
if __name__ == '__main__':
    app.run(debug=True)