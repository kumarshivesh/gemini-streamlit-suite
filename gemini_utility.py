import os
import google.generativeai as genai
from PIL import Image

from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Access the GEMINI API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# Configure `google.generativeai` with `GEMINI_API_KEY`
genai.configure(api_key=GEMINI_API_KEY)

# function to load `gemini-pro` model for `ChatBot`
def load_gemini_pro_model():
  gemini_pro_model = genai.GenerativeModel("gemini-pro")
  return gemini_pro_model

# function to load `gemini-1.5-flash` for `Image Captioning`
def gemini_pro_vision_response(prompt, image):
  gemini_pro_vision_model = genai.GenerativeModel("gemini-1.5-flash")
  response = gemini_pro_vision_model.generate_content([prompt, image])
  result = response.text
  return result

#image = Image.open("./src_3/test_image.png")

#prompt = "Write a short caption for this image"

#output = gemini_pro_vision_response(prompt, image)
#print(output)

# function to load `models/embedding-001` for `Embed text`
def embedding_model_response(input_text):
  embedding_model = "models/embedding-001"
  embedding = genai.embed_content(model=embedding_model, content=input_text, task_type="retrieval_document")
  print(embedding)
  embedding_list = embedding["embedding"]
  return embedding_list

#output = embedding_model_response("Who is Thanos")
#print(output)


# function to load `gemini-pro` model for `Ask me anything`
def gemini_pro_response(user_prompt):
  gemini_pro_model = genai.GenerativeModel("gemini-pro")
  response = gemini_pro_model.generate_content(user_prompt)
  result = response.text
  return result

#output = gemini_pro_response("What is Machine Learning")
#print(output)

