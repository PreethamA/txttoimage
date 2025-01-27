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
#j.save("C:/Users/User/Desktop/mesh_trans",".bmp")
"""
import torch
from diffusers import FluxPipeline

# Replace with your actual access token
hf_access_token = "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"

# Load the model with access token
pipe = FluxPipeline.from_pretrained(
    "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev",
    revision="fp16",  # Optional: Specify model revision (if applicable)
    use_auth_token=hf_access_token,
    torch_dtype=torch.bfloat16,
)

pipe.enable_model_cpu_offload()

prompt = "A cat holding a sign that says hello world"
image = pipe(
    prompt,
    height=1024,
    width=1024,
    guidance_scale=3.5,
    num_inference_steps=50,
    max_sequence_length=512,
    generator=torch.Generator("cpu").manual_seed(0)
).images[0]
image.save("flux-dev.png")
"""