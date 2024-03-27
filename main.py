from flask import Flask, render_template, request, jsonify
from io import BytesIO
import base64
import text2image
from p_square_chat import chat
from PIL import Image
import os
from googletrans import Translator


ASSETS_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)


@app.route('/')
def main():
    return render_template("main.html")


@app.route('/text2image')
def texttoimage():
    return render_template('text2image.html')


@app.route('/text2image', methods=['POST'])
def generate_image():
    if request.method == 'POST':
        option = get_selection_input()
        option_input = get_text_input()

        # Prompt
        prompt = option + option_input
        prompt = ', '.join(prompt)
        # Translate to Chinese
        text_input = translate(prompt)

        # Generate image
        generated_image = generate_image_from_text(text_input)

        # Error Handling
        if type(generated_image) == str:
            return render_template('text2image.html', generated_image_base64="", text_input=generated_image)
        else:
            generated_image_ = []
            for i in range(0, len(generated_image)):
                # Convert PIL image to base64 string
                generated_image_.append(pil_to_base64(generated_image[i]._pil_image.resize(
                    (1024, 1024), resample=Image.LANCZOS)))

            if len(generated_image_) > 3:
                return render_template('text2image.html',
                                       base64_encoded_image_1=generated_image_[
                                           0],
                                       base64_encoded_image_2=generated_image_[
                                           1],
                                       base64_encoded_image_3=generated_image_[
                                           2],
                                       base64_encoded_image_4=generated_image_[
                                           3],
                                       text_input=text_input)
            elif len(generated_image) == 3:
                return render_template('text2image.html',
                                       base64_encoded_image_1=generated_image_[
                                           0],
                                       base64_encoded_image_2=generated_image_[
                                           1],
                                       base64_encoded_image_3=generated_image_[
                                           2],
                                       text_input=text_input)

            elif len(generated_image) == 2:
                return render_template('text2image.html',
                                       base64_encoded_image_1=generated_image_[
                                           0],
                                       base64_encoded_image_2=generated_image_[
                                           1],
                                       text_input=text_input)
            else:
                return render_template('text2image.html',
                                       base64_encoded_image_1=generated_image_[
                                           0],
                                       text_input=text_input)


def get_selection_input():
    # get select option
    characters = request.form['characters']
    faces = request.form['faces']
    background = request.form['background']
    action = request.form['action']
    style = request.form['style']
    clothes = request.form['clothes']
    look = request.form['look']
    say_something = "圖片上的文字： " + \
        request.form['say_something'] if request.form['say_something'] != "無" else "無"

    options = [characters, faces, background,
               action, style, clothes, look, say_something]

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
    style_input = request.form['style_input']
    clothes_input = request.form['clothes_input']
    look = request.form['look_input']
    say_something = "圖片上的文字： " + \
        request.form['word_on_picture'] if request.form['word_on_picture'] != "" else ""
    option_input = [character_input, face_input,
                    action_input, background_input, style_input, clothes_input, look, say_something]

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


@app.route('/SquareSyncAI')
def squaresyncai():
    return render_template('chat.html')


@app.route('/api/chat', methods=['POST'])
def chat_response():
    data = request.json
    user_message = data.get('message')

    bot_response = chat(user_message)

    return jsonify({'message': bot_response})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
