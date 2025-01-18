import os
from typing import List
import textract
import google.generativeai as genai
from dotenv import load_dotenv, find_dotenv
import ast


def extract_text_from_document(doc_path: str):
    text = textract.process(doc_path)
    return text

def get_product_info(
   language: str, file_path: str = None, text: str = None
) -> str:
    load_dotenv(find_dotenv())
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-flash")

    llm_prompt = """
        <instructions>
            Analyze the provided content and extract detailed product information in the following format:
            
            1. Generate a clear, specific product category
            2. Extract key product features and specifications
            3. Identify the target audience or use case
            4. Determine relevant search keywords
            5. List similar product categories to consider
            
            Format the response as a valid Python dictionary with the following keys:
            {
                "category": "main product category",
                "subcategories": ["relevant", "subcategories"],
                "features": ["key", "product", "features"],
                "target_audience": ["primary", "user", "groups"],
                "search_terms": ["specific", "search", "terms"],
                "similar_categories": ["related", "product", "types"]
            }
            
            Guidelines:
            - Be specific and detailed in categorization
            - Focus on objective, searchable features
            - Include both technical and practical characteristics
            - Consider multiple use cases and user groups
            - Generate search-optimized terms
            
            Return only the Python dictionary, no additional text.
        </instructions>
        """

    # llm_prompt += f"\n\n<!-- Please make the script so that it {video_preference} the content. -->"

    # Adding the language conditionally
    if language != "English":
        llm_prompt += f"\n\n<!-- Please make the script in {language}. -->"

    if text:
        # Use text directly if provided
        llm_prompt += f"\n\nContent:\n{text}"
        response = model.generate_content([llm_prompt])
    else:
        # Determine the file type
        file_extension = os.path.splitext(file_path)[-1].lower()

        if file_extension == ".pdf":
            # Directly upload PDF files
            pdf = genai.upload_file(file_path)
            response = model.generate_content([llm_prompt, pdf])

        elif file_extension in [".jpg", ".jpeg", ".png"]:
            # For image files, pass them directly
            sample_image = genai.upload_file(file_path)
            response = model.generate_content([llm_prompt, sample_image])

        elif file_extension in [".doc", ".docx", ".pptx"]:
            document_text = extract_text_from_document(file_path)
            llm_prompt += f"\n\nContent:\n{document_text}"
            response = model.generate_content([llm_prompt])

        else:
            raise ValueError("Unsupported file type.")

    return response.text