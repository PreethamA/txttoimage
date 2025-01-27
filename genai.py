import requests
import os

from dotenv import load_dotenv,find_dotenv

load_dotenv(find_dotenv(".env"))
API_URL = os.environ.get("API_URL")
api_key = os.environ.get("api_key")
headers = {"Authorization": f"Bearer {api_key}"}

print(headers)
print(API_URL)
def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.content

image_bytes = query({
	"inputs": "Astronaut riding a donkey",
})

# You can access the image with PIL.Image for example
import io
from PIL import Image

j = Image.open(io.BytesIO(image_bytes))
j.save('out.png')
