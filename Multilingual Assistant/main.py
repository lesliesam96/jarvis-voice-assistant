import speech_recognition as sr
import logging
import os
from gtts import gTTS
from google import genai
import streamlit as st


# This is Logger for the application
LOG_DIR = "logs"
LOG_FILE_NAME = "application.log"

os.makedirs(LOG_DIR, exist_ok=True)

log_path = os.path.join(LOG_DIR, LOG_FILE_NAME)

logging.basicConfig(
    filename=log_path,
    format="[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


def takeCommand():
    """This function takes command & recognizes it
    Returns:
        text as query
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-fr")
        print(f"User said: {query}\n")
    except Exception as e:
        logging.info(e)
        print("Say that again please")
        return "None"
    return query


def text_to_speech(text):
    """Convert text to speech and save as mp3"""
    tts = gTTS(text=text, lang="en")
    tts.save("speech.mp3")


def gemini_model(user_input):
    """Send user input to Gemini and return response"""
    client = genai.Client(api_key="YOUR_API_KEY")
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_input
    )
    return response.text


def main():
    st.title("Multilingual AI Assistant")

    if st.button("Ask me anything!"):
        with st.spinner("Listening..."):
            text = takeCommand()

        if text == "None":
            st.warning("I didn't catch that. Please try again.")
        else:
            st.write(f"**You said:** {text}")

            with st.spinner("Thinking..."):
                response = gemini_model(text)

            with st.spinner("Generating speech..."):
                text_to_speech(response)

            # Display response
            st.text_area(label="Response:", value=response, height=350)

            # Display audio player
            audio_file = open("speech.mp3", 'rb')
            audio_bytes = audio_file.read()
            audio_file.close()

            st.audio(audio_bytes, format='audio/mp3')
            st.download_button(
                label="Download Speech",
                data=audio_bytes,
                file_name="speech.mp3",
                mime="audio/mp3"
            )


main()