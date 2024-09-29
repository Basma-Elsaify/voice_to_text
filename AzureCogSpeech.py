import os
import streamlit as st
from audio_recorder_streamlit import audio_recorder
from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer, AudioConfig, AutoDetectSourceLanguageConfig
from azure.cognitiveservices.speech import ResultReason, CancellationDetails
from pydub import AudioSegment

# Set up Azure credentials (using Streamlit secrets for security)
AZURE_SPEECH_KEY = "<REPLACE_WITH_AZURE_SPEECH_KEY>"
AZURE_REGION = "<REPLACE_WITH_REGION>"

# Function to transcribe audio using Azure Cognitive Services Speech with automatic language detection
def transcribe_audio(audio_bytes):
    # Save the recorded audio bytes to a temporary file
    with open("temp_audio.wav", "wb") as f:
        f.write(audio_bytes)

    # Convert to PCM WAV format (required by Azure) with PyDub
    audio = AudioSegment.from_file("temp_audio.wav")
    audio = audio.set_frame_rate(16000).set_channels(1)
    audio.export("temp_audio_converted.wav", format="wav")

    # Azure Speech Configuration
    speech_config = SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_REGION)

    # Enable auto-detection of language with a set of expected languages
    auto_detect_language_config = AutoDetectSourceLanguageConfig(languages=["en-US", "ar-EG"])

    # Set up audio input
    audio_input = AudioConfig(filename="temp_audio_converted.wav")

    # Initialize the speech recognizer with auto language detection
    speech_recognizer = SpeechRecognizer(
        speech_config=speech_config,
        audio_config=audio_input,
        auto_detect_source_language_config=auto_detect_language_config
    )

    # Perform the transcription
    result = speech_recognizer.recognize_once()

    # Clean up temporary files
    os.remove("temp_audio.wav")
    os.remove("temp_audio_converted.wav")

    # Return the transcription result
    if result.reason == ResultReason.RecognizedSpeech:
        # Extract the detected language result
        auto_detect_result = result.properties.get("SpeechServiceConnection_AutoDetectSourceLanguageResult")
        if auto_detect_result:
            detected_language = auto_detect_result.language
        else:
            detected_language = "Unknown"

        return f"Detected Language: {detected_language}\nTranscription: {result.text}"
    elif result.reason == ResultReason.NoMatch:
        return "No speech could be recognized."
    elif result.reason == ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        return f"Error: {cancellation_details.reason}, {cancellation_details.error_details}"
    else:
        return f"Error: {result.reason}"

# Streamlit app layout
st.title("Speech-to-Text with Azure Cognitive Services")
st.write("Record your audio using the button below. The app will automatically detect and transcribe either Arabic or English.")

# Create columns for input and recording
col1, col2 = st.columns([4, 1])

with col1:
    user_input = st.text_input("Type your message here (optional):")

with col2:
    st.write("")  # For alignment
    audio_bytes = audio_recorder(pause_threshold=0.8, icon_size=3)

# Handle audio input
if audio_bytes:
    with st.spinner("Transcribing audio..."):
        transcription = transcribe_audio(audio_bytes)
        st.write("Transcription:")
        st.write(transcription)

# Handle text input (for demonstration purposes)
if user_input:
    st.write(f"Echo: {user_input}")
  
