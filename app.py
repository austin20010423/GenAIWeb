from flask import Flask, render_template, request
from io import BytesIO
import base64
import text2image  # Assuming text2image is your model for converting text to image
import os
from googletrans import Translator

ASSETS_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def generate_image():
    if request.method == 'POST':
        characters = request.form['characters']
        print(characters)

        # Translate to Chinese
        '''text_input = translate(text_input)
        negative_input = translate(negative_input)'''

        # Generate image
        # generated_image = generate_image_from_text(text_input, negative_input)
'''
        # Error Handling
        if type(generated_image) == str:
            return render_template('index.html', generated_image_base64="", text_input=generated_image)
        else:
            # Convert PIL image to base64 string
            generated_image_base64 = pil_to_base64(generated_image)
            return render_template('index.html', generated_image_base64=generated_image_base64, text_input=text_input)
'''


def translate(text: str):
    translator = Translator()
    translated = translator.translate(text, dest='en')
    print("Prompt: ", translated.text)
    return translated.text


def generate_image_from_text(text, negative_input):
    # Assuming text2image.model(text) returns a PIL image object
    image = text2image.model(text, negative_input)
    return image


def pil_to_base64(pil_image):
    # Convert PIL image to base64 string
    buffered = BytesIO()
    pil_image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


if __name__ == '__main__':
    context = ('server.crt', 'server.key')
    app.run(debug=True, host='0.0.0.0', port='8080',
            ssl_context=context)
