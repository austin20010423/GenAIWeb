from flask import Flask, render_template, request
from io import BytesIO
import base64
import text2image  
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
        option = get_selection_input()
        option_input = get_text_input()
        word_on_picture = request.form['word_on_picture']

        # Prompt

        prompt = option + option_input
        prompt = ', '.join(prompt) + word_on_picture
        # Translate to Chinese
        text_input = translate(prompt)

        # Generate image
        generated_image = generate_image_from_text(text_input)

        # Error Handling
        if type(generated_image) == str:
            return render_template('index.html', generated_image_base64="", text_input=generated_image)
        else:
            # Convert PIL image to base64 string
            generated_image_base64 = pil_to_base64(generated_image)
            return render_template('index.html', generated_image_base64=generated_image_base64, text_input=text_input)


def get_selection_input():
    # get select option
    characters = request.form['characters']
    faces = request.form['faces']
    background = request.form['background']
    action = request.form['action']
    options = [characters, faces, background, action]

    try:
        element_to_remove = "無"
        options = [x for x in options if x != element_to_remove]

    except:
        pass

    return options


def get_text_input():
    character_input = request.form['character_input']
    face_input = request.form['face_input']
    action_input = request.form['action_input']
    background_input = request.form['background_input']
    option_input = [character_input, face_input,
                    action_input, background_input]

    try:
        element_to_remove = ""
        option_input = [x for x in option_input if x != element_to_remove]

    except:
        pass

    return option_input


# Translate to English
def translate(text: str):
    translator = Translator()
    translated = translator.translate(text, dest='en')
    print("Prompt: ", translated.text)
    return translated.text


def generate_image_from_text(text, negative_input=None):
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
