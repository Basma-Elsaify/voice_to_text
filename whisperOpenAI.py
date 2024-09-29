import streamlit as st
import openai
from openai import OpenAI
from pydub import AudioSegment
import os
from audio_recorder_streamlit import audio_recorder

OPENAI_KEY = "<REPLACE_WITH_OPENAI_KEY>"
openai.api_key = OPENAI_KEY
client = OpenAI(api_key=OPENAI_KEY)


# Function to process and transcribe audio using OpenAI Whisper API
def transcribe_audio(audio_bytes):
    # Save the recorded audio bytes to a temporary file
    with open("temp_audio.wav", "wb") as f:
        f.write(audio_bytes)
    
    # Convert the audio file to MP3 format for OpenAI Whisper API
    audio = AudioSegment.from_file("temp_audio.wav")
    audio.export("temp_audio.mp3", format="mp3")

    # Open the exported audio file and send it to OpenAI for transcription
    with open("temp_audio.mp3", "rb") as file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1", 
            file=file,
            prompt="<REPLACE_WITH_SPECIAL_WORDS_LIKE_RELEVANT_UNCOMON_COMPANY_OR_PRODUCT_NAME>"
            # response_format='text'
        )

    # Clean up the temporary audio files
    os.remove("temp_audio.wav")
    os.remove("temp_audio.mp3")
    return transcription.text

# Audio recording section
st.write("Please record your audio below:")
audio_bytes = audio_recorder()

if audio_bytes:
    with st.spinner("Transcribing..."):
        transcription = transcribe_audio(audio_bytes)
        # st.audio(audio_bytes, format="audio/wav") # This line to to play the recorded audio
        st.write("Transcription:")
        st.write(transcription)
else:
    st.write("Click the button above to record your audio.")
