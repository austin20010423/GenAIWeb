from vertexai.preview.generative_models import GenerativeModel
from detect_intent import run_dialogflow
from google.cloud import texttospeech
import shutil


def run_chat_gemini(message: str):

    gemini_pro_model = GenerativeModel("gemini-1.0-pro")
    model_response = gemini_pro_model.generate_content(
        f"Your general instruction: <用繁體中文跟我對話> Answer the user message: <{message}>")
    # print("model_response\n", model_response.text)
    return model_response.text


def chat(message: str):
    response = run_dialogflow(message)

    if response == "對不起，我聽不懂你的問題。":
        response = run_chat_gemini(message)
    audio_data = synthesize_text(response)

    return response


def synthesize_text(text, output_file="/tmp/chat.wav"):
    # Create a TextToSpeechClient
    client = texttospeech.TextToSpeechClient()

    # Set the text input
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Set the voice parameters
    voice = texttospeech.VoiceSelectionParams(

        language_code="cmn-TW",
        name="cmn-TW-Standard-A",  # You can change the voice based on your preferences
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Set the audio output configuration
    audio_config = texttospeech.AudioConfig(
        pitch=2,
        speaking_rate=1,
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )

    # Synthesize the speech
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response

    """# Save the synthesized audio to a file
    with open(output_file, "wb") as out:
        out.write(response.audio_content)
        print("=" * 20)
        print(f'Audio content written to file "{output_file}"')"""
