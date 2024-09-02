import speech_recognition as sr
from Text2SpeechEn import text_to_speech_stream

def listen_and_transcribe():
    # Recognizer ve mikrofonu başlat
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    # Mikrofondan ses almak için ayarlamalar yap
    with microphone as source:
        print("Talk...")
        #recognizer.adjust_for_ambient_noise(source)
       # audio = recognizer.listen(source)
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source )

    try:
        # Google'ın ses tanıma API'si ile sesi metne çevir
        text = recognizer.recognize_google(audio, language='en-EN')
        return text
    except sr.UnknownValueError:
        text="Sory I could not understand audio."
        return text
    except sr.RequestError:
        print("Servise was not found")

if __name__ == "__main__":
    listen_and_transcribe()


