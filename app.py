from flask import Flask, render_template, request, send_from_directory
import os
from PIL import Image, ImageDraw, ImageFont
import requests
import io
from datetime import datetime

from dotenv import load_dotenv,find_dotenv

load_dotenv(find_dotenv(".env"))
API_URL = os.environ.get("API_URL")
api_key = os.environ.get("api_key")
headers = {"Authorization": f"Bearer {api_key}"}

app = Flask(__name__)

# Directory to store generated images
UPLOAD_FOLDER = 'static/generated_images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create the directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.content

@app.route('/', methods=['GET', 'POST'])
def index():
    image_path = None
    if request.method == 'POST':
        text = request.form['text']
        if text:
            image_path = query(text)  # Generate and save the image
            j = Image.open(io.BytesIO(image_path))

            image_path = os.path.join(app.config['UPLOAD_FOLDER'], os.path.basename(j.save(f'out_'+{datetime.now.strftime("%d_%m_%Y_%H_%M_%S")}+'.png')))  # Path relative to static folder. Important for send_from_directory

            # You could also return the image data directly (base64 encoded) to avoid saving to disk, but it's more complex.
            # See the alternative example below.

    return render_template('index.html', image_path=image_path)


def generate_image(text):
    # Create a blank image
    img_width = 800  # Adjust as needed
    img_height = 200  # Adjust as needed
    img = Image.new('RGB', (img_width, img_height), color=(255, 255, 255))  # White background
    draw = ImageDraw.Draw(img)

    # Choose a font (you might need to install fonts)
    try:
        font = ImageFont.truetype("arial.ttf", size=30)  # Try Arial first.  If that fails...
    except IOError:
        font = ImageFont.load_default()  # Fallback to a default font if Arial isn't found.

    # Calculate text size and position
    text_width, text_height = draw.textsize(text, font=font)
    x = (img_width - text_width) // 2  # Center horizontally
    y = (img_height - text_height) // 2  # Center vertically

    # Draw the text
    draw.text((x, y), text, fill=(0, 0, 0), font=font)  # Black text

    # Save the image
    image_filename = "generated_image_"++".png"  # Or use a timestamp for unique names
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
    img.save(image_path)

    return image_path


# Serve static files (including generated images)
@app.route('/' + app.config['UPLOAD_FOLDER'] + '/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)

