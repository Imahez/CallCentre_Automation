import streamlit as st
import time
import speech_recognition as sr
from pydub import AudioSegment
import tempfile

@st.cache_data
def transcribe_audio(audio_file):
    # Convert audio file to WAV if necessary
    if audio_file.type == "audio/m4a":
        # Create a temporary WAV file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
            audio = AudioSegment.from_file(audio_file, format="m4a")
            audio.export(temp_wav.name, format="wav")
            audio_file = temp_wav.name  # Use the temp WAV file for transcription

    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)  # Read the entire audio file
        return recognizer.recognize_google(audio)  # Use Google Web Speech API
    except sr.UnknownValueError:
        return "Sorry, I could not understand the audio."
    except sr.RequestError as e:
        return f"Could not request results from the speech recognition service; {e}"
    except Exception as e:
        return f"An error occurred: {e}"

def main():
    st.title('Chat Bot')

    uploaded_audio = st.file_uploader("Upload your audio question", type=["wav"])

    submit_button = st.button('Submit')
    input_text = None  # Initialize input_text

    if submit_button and uploaded_audio:
        with st.spinner(text='Processing...'): 
            time.sleep(2)  # Simulate processing time
            input_text = transcribe_audio(uploaded_audio)

    if input_text:
        # Generate a response for any topic
        response_text = input_text
        st.header('Response:')
        st.write(response_text)

if __name__ == "__main__":
    main()
