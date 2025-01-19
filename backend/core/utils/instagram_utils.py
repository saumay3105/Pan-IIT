import os
from instagrapi import Client
from dotenv import load_dotenv
import google.generativeai as genai


def post_on_insta(image_location, caption):
    cl = Client()
    cl.login("team.bigo4", "threesome")

    user_id = cl.user_id_from_username("team.bigo4")
    cl.photo_upload(image_location, caption)


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-flash")


def generate_caption(trends, content):
    try:
        prompt = f"""
        Given the trending hashtags: {trends}, create an engaging and attention-grabbing caption for the following content: {content}. 
        Ensure the caption is relevant, popular, and likely to attract a wide audience.
        Deduce the meaning of these hashtags and generate fun and creative captions. Use a few relevant hashtags from the list to boost the post's reach.
        Use English language only.
        For example, if there is a trending hashtag about football and the content is about career growth, you could create a caption like, "#Barcelona didn’t settle, neither should you. Play every move in your #career like it's a Champions League final!"
        Avoid using irrelevant hashtags; only use those that align with the trending topics.
        Return a single caption with relevant hashtags and nothing else.
        Avoid political content.
        """
        response = model.generate_content([prompt])
        return response.text

    except Exception as e:
        print(f"Error interacting with Gemini API: {e}")
        return None


def generate_post_content(content):
    prompt = f"""
    Given the following content {content}, generate post data for social media. Give me ideas for two posts.
    In the following, manner
    [{{
        heading: "Bajaj Allianz", # Company name if provided else the main topic of the content (Max char 18)
        subtitle: "Insurance Company", # Relevant subtitle (Max words 5)
        button: "Read More", # Call to action button description (Max words 2)
        description: "Fuel your dreams, not your debt!", # Short and cocise description (Max words 6-7)
        address: "info@bajajfinserv.com", # Email or any website provided, if not provided then return something important (Max words 2)
        image_keyword: "educational loan", # Keyword for the image to be generated
    }}, 
    {{
        heading: "Bajaj Allianz", # Company name if provided else the main topic of the content (Max char 18)
        subtitle: "Insurance Company", # Relevant subtitle (Max words 5)
        button: "Read More", # Call to action button description (Max words 2)
        description: "Fuel your dreams, not your debt!", # Short and cocise description (Max words 6-7)
        address: "info@bajajfinserv.com", # Email or any website provided, if not provided then return something important (Max words 2)
        image_keyword: "educational loan", # Keyword for the image to be generated
    }}
    ]

    Return only the list with two dictionary and nothing else.
    """
    response = model.generate_content([prompt])

    try:
        # Generate the content using the model
        response_text = response.text

        # Find the start and end of the list in the response text
        start_index = response_text.find("[")
        end_index = response_text.rfind("]") + 1

        # Extract the list from the response text
        list_str = response_text[start_index:end_index]

        # Convert the string representation of the list to an actual list
        post_data = eval(list_str)

        return post_data

    except Exception as e:
        print(f"Error processing the response: {e}")
        return None
