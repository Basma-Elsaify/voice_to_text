import streamlit as st
import speech_recognition as sr

# Initialize the recognizer
recognizer = sr.Recognizer()

# Streamlit application
def main():
    st.title("Voice to Text Application")
    st.write("Click the button below and start speaking. The application supports both English and Arabic.")

    # Button to start recording
    if st.button("Record Voice"):
        with sr.Microphone() as source:
            st.write("Listening...")
            audio_data = recognizer.listen(source)
            st.write("Processing...")

            try:
                # Attempt to recognize speech in English
                text_en = recognizer.recognize_google(audio_data, language="en-US")
                st.success(f"Recognized in English: {text_en}")
            except sr.UnknownValueError:
                st.warning("Could not understand audio in English.")
            
            try:
                # Attempt to recognize speech in Arabic
                text_ar = recognizer.recognize_google(audio_data, language="ar-SA")
                st.success(f"Recognized in Arabic: {text_ar}")
            except sr.UnknownValueError:
                st.warning("Could not understand audio in Arabic.")
            except sr.RequestError as e:
                st.error(f"Could not request results; {e}")

if __name__ == "__main__":
    main()
