from dotenv import load_dotenv
from imagekitio import ImageKit
import os

load_dotenv() # looks for presence of .env vars

imagekit = ImageKit(
    private_key=os.getenv("IMAGEKIT_PRIVATE_KEY")
)

URL_ENDPOINT = os.getenv("IMAGEKIT_URL_ENDPOINT")