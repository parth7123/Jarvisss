import asyncio
import os
import logging
from random import randint
from PIL import Image
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("HuggingFaceAPIKey")
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {API_KEY}"}

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

SAVE_PATH = r"C:\\Users\\parth\\Desktop\\Jarvis\\Data"
os.makedirs(SAVE_PATH, exist_ok=True)

def open_images(prompt):
    """Opens and displays generated images."""
    prompt = prompt.replace(" ", "_")
    files = [f"{prompt}{i}.jpg" for i in range(1, 5)]
    
    for jpg_file in files:
        image_path = os.path.join(SAVE_PATH, jpg_file)
        try:
            img = Image.open(image_path)
            logging.info(f"Opening image: {image_path}")
            img.show()
        except IOError:
            logging.warning(f"Unable to open {image_path}")

async def query(payload):
    """Sends a query to Hugging Face API asynchronously."""
    response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
    return response.content

async def generate_images(prompt):
    """Generates images asynchronously."""
    tasks = [
        asyncio.create_task(query({
            "inputs": f"{prompt}, quality=4K, sharpness=maximum, Ultra High details, high resolution, seed={randint(0, 1000000)}"
        })) for _ in range(4)
    ]
    image_bytes_list = await asyncio.gather(*tasks)
    for i, image_bytes in enumerate(image_bytes_list):
        with open(os.path.join(SAVE_PATH, f"{prompt.replace(' ', '_')}{i + 1}.jpg"), "wb") as f:
            f.write(image_bytes)

async def generate_and_open_images(prompt):
    """Runs the image generation process and displays images asynchronously."""
    await generate_images(prompt)
    open_images(prompt)

# Allow function calls from main.py
if __name__ == "__main__":
    prompt = input("Enter the image prompt: ").strip()
    if prompt:
        asyncio.run(generate_and_open_images(prompt))
    else:
        logging.warning("No prompt provided. Exiting.")
