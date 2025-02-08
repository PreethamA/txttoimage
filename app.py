from flask import Flask, render_template, request, jsonify
import requests
import base64
import os
import io
from PIL import Image

from dotenv import load_dotenv,find_dotenv

load_dotenv(find_dotenv(".env"))
API_URL = os.environ.get("API_URL")
api_key = os.environ.get("api_key")
headers = {"Authorization": f"Bearer {api_key}"}

app = Flask(__name__)

# Replace with your actual inference API endpoint
#INFERENCE_API_URL = "YOUR_INFERENCE_API_ENDPOINT"  # e.g., "http://your-inference-server/infer"

@app.route("/", methods=["GET", "POST"])
def index():
    image_data = None
    error_message = None

    if request.method == "POST":
        text = request.form.get("text")

        if not text:
            error_message = "Please enter text."
        else:
            try:
                # Send text to inference API
                payload = {"inputs": text}  # Adjust payload structure if needed
                response = requests.post(API_URL,headers=headers, json=payload)
                print(response.content)
                image_bytes = response.content
                # Use PIL (Pillow) to open the image from bytes
                image = Image.open(io.BytesIO(image_bytes))

                # Convert the image to base64 for display in HTML
                buffered = io.BytesIO()
                image.save(buffered, format="JPEG")  # Or PNG, GIF, etc. - match your image type
                image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

                image_data = image_base64  # image_data is now a base64 string

            except requests.exceptions.RequestException as e:
                error_message = f"Error communicating with inference API: {e}"
            except Exception as e:
                error_message = f"An unexpected error occurred: {e}"


    return render_template("index.html", image_data=image_data, error_message=error_message)


if __name__ == "__main__":
    app.run(debug=True)  # Set debug=False in production
