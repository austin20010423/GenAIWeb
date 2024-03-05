from flask import Flask, render_template, request
from io import BytesIO
import base64
import text2image  # Assuming text2image is your model for converting text to image

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate_image', methods=['POST'])
def generate_image():
    if request.method == 'POST':
        text_input = request.form['text_input']
        negative_input = request.form['negative_prompt']
        generated_image = generate_image_from_text(text_input, negative_input)
        # Convert PIL image to base64 string
        generated_image_base64 = pil_to_base64(generated_image)
        return render_template('result.html', generated_image_base64=generated_image_base64, text_input=text_input)


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
    app.run(debug=True, host='0.0.0.0', port='8080')
