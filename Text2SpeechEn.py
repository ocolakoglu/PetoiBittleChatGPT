import requests
import base64
from pydub import AudioSegment
from pydub.playback import play
import io

def text_to_speech_stream(text):
    api_key = "AIzaSyC17dnNbnSO6WRa6ZNgwJDgfrCSUThqidc"
    # Google Text-to-Speech API endpoint
    url = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={api_key}"

    # İstek verisi (JSON formatında)
    data = {
        "input": {"text": text},
        "voice": {
            "languageCode": "en-US",  # Türkçe dil kodu
            "ssmlGender": "MALE"  # Erkek sesi
        },
        "audioConfig": {
            "audioEncoding": "MP3",  # Çıkış formatı MP3
            "speakingRate": 1  # Konuşma hızı
        }
    }

    # Send post request to api
    response = requests.post(url, json=data)

    # Check the response
    if response.status_code == 200:
        # Get the voice
        audio_content = response.json().get("audioContent")

        if audio_content:

            audio_data = base64.b64decode(audio_content)


            audio_stream = io.BytesIO(audio_data)


            sound = AudioSegment.from_file(audio_stream, format="mp3")
            play(sound)
        else:
            print("Error:")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)


