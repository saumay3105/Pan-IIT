from dotenv import load_dotenv
import os
import google.generativeai as genai

def generate_text(prompt, model="text-bison-001"):
  """
  Generates text using the Gemini API.

  Args:
    prompt: The prompt for the Gemini model.
    model: The Gemini model to use (e.g., "text-bison-001", "Gemini-Pro").

  Returns:
    The generated text.
  """
  try:
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    genai.configure(api_key=api_key)

    response = genai.generate_text(prompt=prompt, model=model)
    return response.text 

  except Exception as e:
    print(f"Error interacting with Gemini API: {e}")
    return None