import tempfile
try:
    import speech_recognition as sr
    from gtts import gTTS
    import playsound
except ImportError:
    sr = None

def speech_to_text():
    if sr is None:
        return input("Say or type expense: ")
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        return r.recognize_google(audio)
    except:
        return input("Couldn't recognize. Type instead: ")

def text_to_speech(text):
    if sr is None:
        print("BOT:", text)
        return
    tts = gTTS(text=text, lang="en")
    with tempfile.NamedTemporaryFile(delete=True) as fp:
        path = f"{fp.name}.mp3"
        tts.save(path)
        playsound.playsound(path)

