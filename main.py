import os
import pathlib
import textwrap

import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

def to_markdown(text):
    text = text.replace('+', '*')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Set up Streamlit app
st.set_page_config(
    page_title="Welcome to LLM Deepmind Era 🚀",
    page_icon="🌌",
    layout="wide"
)

# Introduction
st.title("Welcome to LLM Deepmind Era!")
st.markdown("""
    Hello, I'm Hakim, a student at BSPU in CST, aspiring to be a Machine Learning Engineer.
    I've developed this project, LLM Deepmind Era, as part of my machine learning journey.
    Feel free to explore and enjoy the capabilities of this Large Language Model (LLM) powered by the Google API.
    Connect with me on GitHub and Kaggle to discover more about my projects and contributions.
""")

# Links to GitHub and Kaggle
st.markdown("GitHub: [DreamIsMl](https://github.com/DreamIsMl) 🚀")
st.markdown("Kaggle: [hakim11](https://www.kaggle.com/hakim11) 📊")

# Sidebar navigation
selected_page = st.sidebar.radio("Select a page", ["Content Creator", "Chat Assistant", "Content Creation with Image"])

# Display selected page
if selected_page == "Content Creator":
    st.title('✨ Content Creator AI')
    input_text_content = st.text_input('Enter your question or topic: ', key='input_content')
    submit_button_content = st.button("Generate Content")

    if submit_button_content:
        try:
            model_content = genai.GenerativeModel('gemini-pro')
            response_text_content = model_content.generate_content(input_text_content).text

            st.subheader('Generated Content:')
            st.markdown(to_markdown(response_text_content))

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

elif selected_page == "Chat Assistant":
    st.title("🤖 Chat Assistant")
    input_text_chat = st.text_input("Input: ", key="input_chat")
    submit_button_chat = st.button("Send")

    if submit_button_chat:
        try:
            model_chat = genai.GenerativeModel('gemini-pro')
            chat = model_chat.start_chat(history=[])

            response_chat = chat.send_message(input_text_chat, stream=True)

            # Display chat history
            st.subheader("Chat History:")
            for message in chat.history:
                role = message.role
                text = message.parts[0].text
                st.write(f"{role.capitalize()}: {text}")

            # Display the model's response
            st.subheader("The Response is:")
            for chunk in response_chat:
                st.write(chunk.text)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

elif selected_page == "Content Creation with Image":
    st.title("Content Creation with Image 🖼️")
    st.markdown("""
        Upload an image and provide a prompt to generate creative content!
        Let the AI create a story or description based on your input.
    """)

    # Input components
    input_prompt_image = st.text_area("Input Prompt:", key="input", height=150)
    uploaded_file_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    # Display the uploaded image
    if uploaded_file_image is not None:
        image_image = Image.open(uploaded_file_image)
        st.image(image_image, caption="Uploaded Image.", use_column_width=True)

    # Button to generate content
    generate_button_image = st.button("Tell me about the image")

    # Generate content on button click
    if generate_button_image:
        try:
            model_image = genai.GenerativeModel('gemini-pro-vision')
            input_text_image = st.text_input("Additional Input (Optional): ", key="input_image")
            if input_text_image != "":
                response_image = model_image.generate_content([input_prompt_image, input_text_image, image_image]).text
            else:
                response_image = model_image.generate_content([input_prompt_image, image_image]).text

            st.subheader("Generated Content:")
            st.markdown(to_markdown(response_image))

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Section at the bottom of the left sidebar
st.sidebar.markdown("## AI Capabilities")
st.sidebar.markdown("- Chat 🤖")
st.sidebar.markdown("- Generate Content ✨")
st.sidebar.markdown("- Generate Content with AI 🚀")
st.sidebar.markdown("- Translation 🌐")
st.sidebar.markdown("- and more...")

