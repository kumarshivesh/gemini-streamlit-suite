# pip install streamlit
# pip install streamlit-option-menu
# pip install google-generativeai
# pip install pillow
# pip install python-dotenv

import os

import streamlit as st
from streamlit_option_menu import option_menu
from gemini_utility import load_gemini_pro_model, gemini_pro_vision_response, embedding_model_response, gemini_pro_response
from PIL import Image

# https://emojipedia.org/
# https://icons.getbootstrap.com/


# Configuring Streamlit Page Settings

st.set_page_config(
  page_title="Gemini AI",
  page_icon="🧠",
  layout="centered"
)

with st.sidebar:
  selected = option_menu("Gemini AI", ["ChatBot", "Image Captioning", "Embed text", "Ask me anything"],
                          menu_icon='robot', 
                          icons=['chat-dots-fill', 'image-fill', 'textarea-t','patch-question-fill'],                
                          default_index=0)

# Function to translate role `gemini-pro` and `streamlit`
def translate_role_for_streamlit(user_role):
  if user_role == 'model':
    return "assistant"
  else:
    return user_role
  
if selected == "ChatBot":

  model = load_gemini_pro_model()

  # Initialize chat session in streamlit if not already present
  if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

  # Streamlit page title
  st.title("🤖 ChatBot")

  # Display the chat history
  for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
      st.markdown(message.parts[0].text)

  # Input field for user's message
  user_prompt = st.chat_input("Ask Gemini Pro...")

  if user_prompt:
    st.chat_message("user").markdown(user_prompt)

    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # display gemini-pro response
    with st.chat_message("assistant"):
      st.markdown(gemini_response.text)


# Image Captioning Page

if selected == "Image Captioning":
    # Streamlit page title
    st.title("📸 Snap Narrate")

    uploaded_image = st.file_uploader("Upload an Image", type=["jpg, jpeg", "png"])

    # Add input field for the prompt
    user_prompt = st.text_input("Enter a prompt for the image caption:", "Write a short caption for this image")

    if st.button("Generate Caption") and uploaded_image is not None:
        image = Image.open(uploaded_image)

        col1, col2 = st.columns(2)

        with col1:
            resized_image = image.resize((800, 500))
            st.image(resized_image)

        # Use the user-provided prompt instead of a default one
        caption = gemini_pro_vision_response(user_prompt, image)

        with col2:
            st.info(caption)
    elif uploaded_image is None:
        st.error("Please upload an image before generating a caption.")


# Text Embedding Page
if selected == "Embed text":
   
   st.title("🔡 Embed Text")

   # Input Text Box
   input_text = st.text_area(label="Text Input", placeholder="Enter the text to get the embeddings")

   if st.button("Get Embeddings"):
      response = embedding_model_response(input_text)
      st.markdown(response)

# Ask me anything Page
if selected == "Ask me anything":
   
   st.title("❓ Ask me a question")

   # Text box to enter prompt
   user_prompt = st.text_area(label="Text Input", placeholder="Ask Gemini Pro...")

   if st.button("Get an answer"):
      response = gemini_pro_response(user_prompt)
      st.markdown(response)