from googletrans import Translator

translator = Translator()
translated = translator.translate(["嗨你好", "如何"], dest='en')
print("Prompt: ", translated.text)
