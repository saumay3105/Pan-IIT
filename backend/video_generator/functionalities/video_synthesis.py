import os
import google.generativeai as genai
import azure.cognitiveservices.speech as speechsdk
from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip
from moviepy.editor import ImageClip, concatenate_videoclips
from PIL import Image, ImageDraw
from io import BytesIO
import aiohttp
import numpy as np
from video_generator.functionalities.text_processing import generate_keywords
from video_generator.functionalities.text_processing import generate_keywords_fast
from dotenv import load_dotenv, find_dotenv
import requests
import random
import ast

load_dotenv(find_dotenv())

unsplash_api_key = os.environ["UNSPLASH_API_KEY"]
pixabay_api_key = os.environ["PIXABAY_API_KEY"]


def generate_text(text: str, context_list: list):

    GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")

    llm_prompt = f"""
    Given the following text:
    
    {text}

    For each element in the context list below, generate one factual, descriptive, and clear sentence that matches 
    the context of that element. Each sentence should not exceed 25 words and should not be less than a complete sentence of 10 words. 
    Ensure the sequence of the output list aligns with the input list.

    Context list:
    {context_list}

    Output a Python list of generated sentences corresponding to the context list.
    """

    response = model.generate_content(llm_prompt)
    start_idx = response.text.find("[")
    end_idx = response.text.rfind("]") + 1
    trimmed_response = response.text[start_idx:end_idx]

    return ast.literal_eval(trimmed_response)


async def fetch_image_from_unsplash(session, keyword):
    url = f"https://api.unsplash.com/search/photos?query={keyword}&client_id={unsplash_api_key}"
    async with session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            num = random.randint(1, 5)
            if data["results"]:
                if data["results"][num]:
                    return data["results"][num]["urls"]["small"]
                return data["results"][0]["urls"]["small"]
    return None


async def fetch_image_from_pixabay(session, keyword):
    url = f"https://pixabay.com/api/?key={pixabay_api_key}&q={keyword}&image_type=photo"
    async with session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            if data["hits"]:
                num = random.randint(1, 5)
                if data["hits"][num]:
                    return data["hits"][num]["largeImageURL"]
                return data["hits"][0]["largeImageURL"]
    return None


async def fetch_image_bytes(session, img_url):
    """
    Fetch the image bytes from the URL.
    """
    async with session.get(img_url) as img_response:
        if img_response.status == 200:
            return await img_response.read()
    return None


# Generate Video using Pollination
def generate_image_from_pollinations(prompt):
    """
    Fetch image bytes from pollinations.ai based on the prompt.
    """
    width = 1300
    height = 1574
    model = "flux"
    seed = random.randint(1, 10000)
    url = f"https://pollinations.ai/p/{prompt}?width={width}&height={height}&seed={seed}&model={model}"
    response = requests.get(url, timeout=200)
    if response.status_code == 200:
        return response.content
    return None


async def fetch_images_as_clips_fast(keywords):
    """
    Fetch images for the given keywords, convert them to in-memory ImageClips,
    and return the list of ImageClips.
    """
    clips = []
    async with aiohttp.ClientSession() as session:
        for keyword in keywords:
            img_url = await fetch_image_from_unsplash(session, keyword)

            if not img_url:
                img_url = await fetch_image_from_pixabay(session, keyword)

            if img_url:
                img_data = await fetch_image_bytes(session, img_url)
                if img_data:
                    img = Image.open(BytesIO(img_data)).convert("RGB")
                    img_np = np.array(img)  # Convert PIL image to NumPy array
                    img_clip = ImageClip(img_np).set_duration(
                        5
                    )  # Set duration of each image to 5 seconds
                    clips.append(img_clip)
                    print(f"Downloaded and added image for keyword: {keyword}")
            else:
                print(f"No images found for: {keyword}")
    return clips


# pollination
async def fetch_images_as_clips(keywords):
    """
    Fetch images from pollinations.ai for the given keywords,
    convert them to in-memory ImageClips, and return the list of ImageClips.
    """
    clips = []

    for keyword in keywords:
        # Get image bytes from pollinations.ai
        img_data = generate_image_from_pollinations(keyword)

        if img_data:
            img = Image.open(BytesIO(img_data)).convert("RGB")
            img_np = np.array(img)  # Convert PIL image to NumPy array
            img_clip = ImageClip(img_np).set_duration(
                6
            )  # Set duration of each image to 5 seconds
            clips.append(img_clip)
            print(f"Generated and added image for keyword: {keyword}")
        else:
            print(f"No image found for: {keyword}")

    return clips


def generate_speech_and_viseme_from_text(
    text: str,
    audio_output_file: str = "output.wav",
    language: str = "English",
):
    load_dotenv(find_dotenv())
    speech_key = os.environ["AZURE_SPEECH_API_KEY"]
    service_region = "eastus"

    # Create a speech configuration object
    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key, region=service_region
    )
    languages = {
        "English": "en-IN",
        "Assamese": "as-IN",
        "Bengali": "bn-IN",
        "Gujarati": "gu-IN",
        "Hindi": "hi-IN",
        "Kannada": "kn-IN",
        "Malayalam": "ml-IN",
        "Marathi": "mr-IN",
        "Nepali": "ne-IN",
        "Punjabi": "pa-IN",
        "Tamil": "ta-IN",
        "Telugu": "te-IN",
        "Urdu": "ur-IN",
    }
    indian_female_voices = {
        "English": "en-IN-NeerjaNeural",
        "Assamese": "as-IN-YashicaNeural",
        "Bengali": "bn-IN-TanishaaNeural",
        "Gujarati": "gu-IN-DhwaniNeural",
        "Hindi": "hi-IN-AnanyaNeural",
        "Kannada": "kn-IN-SapnaNeural",
        "Malayalam": "ml-IN-SobhanaNeural",
        "Marathi": "mr-IN-AarohiNeural",
        "Nepali": "ne-NP-HemkalaNeural",
        "Punjabi": "pa-IN-VaaniNeural",
        "Tamil": "ta-IN-PallaviNeural",
        "Telugu": "te-IN-ShrutiNeural",
        "Urdu": "ur-IN-GulNeural",
    }
    print(indian_female_voices[language])
    # Set the voice based on the teacher's choice
    speech_config.speech_synthesis_voice_name = f"{indian_female_voices[language]}"
    speech_config.speech_synthesis_language = languages[language]

    # Create an audio configuration for saving the audio to a file
    audio_config = speechsdk.audio.AudioOutputConfig(filename=audio_output_file)

    # Create a speech synthesizer object
    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config
    )

    viseme_data = []

    def viseme_callback(evt):
        viseme_data.append(
            [evt.audio_offset / 10000, evt.viseme_id]  # Convert to milliseconds
        )

    # capture visemes
    synthesizer.viseme_received.connect(viseme_callback)

    # Synthesize the text
    result = synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Text-to-speech conversion successful.")
    else:
        print(f"Text-to-speech conversion failed: {result.reason}")
        return None, None

    return viseme_data


async def generate_video_from_script_fast(
    script: str, audio_output_file: str, video_output_file: str
):
    """
    Fetch images for the given keywords and generate a video that matches the length of the audio.
    """
    audio_clip = AudioFileClip(audio_output_file)
    audio_duration = audio_clip.duration  # Get the duration of the audio in seconds
    keywords = generate_keywords_fast(script)
    clips = await fetch_images_as_clips_fast(keywords)

    if clips:
        num_clips = len(clips)
        # Calculate the duration each image should stay on screen
        clip_duration = audio_duration / num_clips

        landscape_clips = []
        for clip in clips:
            img = clip.get_frame(0)  # Get a frame from the clip
            pil_img = Image.fromarray(img)  # Convert to a PIL Image

            # Resize the image to landscape (1280x720) using LANCZOS
            resized_img = pil_img.resize((1280, 720), Image.Resampling.LANCZOS)

            # Convert the resized image back to a NumPy array
            resized_array = np.array(resized_img)

            # Create a new ImageClip from the resized image with the calculated duration
            landscape_clip = ImageClip(resized_array).set_duration(clip_duration)
            landscape_clips.append(landscape_clip)

        # Concatenate the resized landscape clips into a single video
        video_clip = concatenate_videoclips(landscape_clips, method="compose")

        # Add the audio to the video
        final_video = video_clip.set_audio(audio_clip)
        final_video.write_videofile(video_output_file, fps=24)
        print(f"Video saved as {video_output_file}")
    else:
        print("No images to generate video.")


async def generate_video_from_script(
    script: str, audio_output_file: str, video_output_file: str
):
    """
    Fetch images for the given keywords, generate a video with random transitions, and overlay keywords
    at a fixed position (bottom-left or bottom-center) on the images. The video matches the length of the audio.
    """

    audio_clip = AudioFileClip(audio_output_file)
    audio_duration = audio_clip.duration

    keywords = generate_keywords(script)
    texts = generate_text(script, keywords)

    # Fetch image clips based on the keywords
    clips = await fetch_images_as_clips(keywords)

    if clips:
        num_clips = len(clips)
        # Calculate the duration each image should stay on screen based on the audio length
        clip_duration = audio_duration / num_clips

        landscape_clips = []
        for i, clip in enumerate(clips):
            # Get a frame from the clip
            img = clip.get_frame(0)
            pil_img = Image.fromarray(img)

            # Draw a rectangle and place the keyword at the bottom-left or bottom-center
            draw = ImageDraw.Draw(pil_img)
            img_width, img_height = pil_img.size
            rect_width, rect_height = img_width, 80  # Full width of the image
            rect_x, rect_y = (
                0,
                img_height - rect_height - 20,
            )  # Position at the very bottom

            # Draw the rectangle at the fixed position
            draw.rectangle(
                [(rect_x, rect_y), (rect_x + rect_width, rect_y + rect_height)],
                fill="yellow",
            )

            # Overlay the keyword - Handle text wrapping and prevent overflow
            text = texts[i]
            max_font_size = 28
            font = "Arial-Bold"
            wrapped_text = wrap_text(
                text, rect_width - 20, max_font_size, font
            )  # Wrap the text

            # Create the text clip, scale down the font if necessary
            text_clip = TextClip(
                wrapped_text, fontsize=max_font_size, color="red", font=font
            )
            text_clip = text_clip.set_position((rect_x + 10, rect_y + 10)).set_duration(
                clip_duration
            )

            # Convert the image back to a NumPy array
            modified_img = np.array(pil_img)

            # Create a new ImageClip from the modified image with the calculated duration
            image_clip = ImageClip(modified_img).set_duration(clip_duration)

            # Overlay the text on the image
            composite_clip = CompositeVideoClip([image_clip, text_clip])

            landscape_clips.append(composite_clip)

        # Concatenate the clips with random transitions
        video_clip = concatenate_videoclips(landscape_clips, method="compose")

        # Add the audio to the video
        final_video = video_clip.set_audio(audio_clip)

        # Save the final video with the specified output file name
        final_video.write_videofile(video_output_file, fps=24)
        print(f"Video saved as {video_output_file}")
    else:
        print("No images to generate video.")


def wrap_text(text, max_width, font_size, font_name):
    """
    Wrap the text to fit within the rectangle, adjusting the font size as necessary.
    """
    wrapped_text = text
    max_font_size = font_size

    # Try different font sizes to fit the text
    while True:
        text_clip = TextClip(wrapped_text, fontsize=max_font_size, font=font_name)
        text_width, _ = text_clip.size

        # If the text width is within the max allowed width, break
        if text_width <= max_width:
            break
        else:
            max_font_size -= 2

        if max_font_size < 12:
            break

    return wrapped_text


def generate_thumbnail(video_clip, video_duration, thumbnail_output):
    frame = video_clip.get_frame(video_duration / 2)
    thumbnail_image = Image.fromarray(frame)
    thumbnail_image.save(thumbnail_output)

    return thumbnail_output


def generate_video_details(script: str):
    GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    llm_prompt = """
    Given the script, generate a catchy title and description for my video.
    
    {script}
    
    Return me these details in just JSON format and nothing else.  
    """

    response = model.generate_content(llm_prompt)
    return response.text
