
import aiohttp
import asyncio
from PIL import Image
from io import BytesIO
import os

# unsplash_api_key = "9CSLoBXakfx5KFkNd_9nwvgtb3ka1NYIvyhS1w5isWo"
# pixabay_api_key = "45641108-7f535f083ebba7750c58f43d2"


async def fetch_image_from_unsplash(session, keyword):
    url = f"https://api.unsplash.com/search/photos?query={keyword}&client_id={unsplash_api_key}"
    async with session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            if data["results"]:
                return data["results"][0]["urls"]["small"]
    return None


async def fetch_image_from_pixabay(session, keyword):
    url = f"https://pixabay.com/api/?key={pixabay_api_key}&q={keyword}&image_type=photo"
    async with session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            if data["hits"]:
                return data["hits"][0]["largeImageURL"]
    return None


async def download_image(session, img_url, keyword):
    save_folder = "unsplash_images"
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    async with session.get(img_url) as img_response:
        if img_response.status == 200:
            img_data = await img_response.read()
            img = Image.open(BytesIO(img_data))
            # Save the image in the specified folder with the keyword as filename
            img.save(os.path.join(save_folder, f"{keyword}.jpg"))


async def fetch_images(keywords):
    async with aiohttp.ClientSession() as session:
        for keyword in keywords:
            img_url = await fetch_image_from_unsplash(session, keyword)

            if not img_url:
                img_url = await fetch_image_from_pixabay(session, keyword)

            if img_url:
                await download_image(session, img_url, keyword)
                print(f"Downloaded image for keyword: {keyword}")
            else:
                print(f"No images found for: {keyword}")
