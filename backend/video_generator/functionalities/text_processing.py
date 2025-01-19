import os
from typing import List
from collections import Counter
import textract
import google.generativeai as genai
from dotenv import load_dotenv, find_dotenv
import ast


def extract_text_from_document(doc_path: str):
    text = textract.process(doc_path)
    return text


def generate_script(
    video_preference: str, language: str, file_path: str = None, text: str = None
) -> str:
    load_dotenv(find_dotenv())
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-flash")

    llm_prompt = """
        <prompt>
            <step1>Extract the key information and identify the main points that need to be discussed.</step1>
            <step2>Break down these main points into smaller subtopics that can be explained sequentially.</step2>
            <step3>For each subtopic, construct a simple and engaging explanation that fits naturally into a continuous narrative.</step3>
            <step4>Ensure that each subtopic flows logically into the next, maintaining coherence and a clear structure.</step4>
            <step5>Use simple and concise language, keeping the audience's attention with relatable examples or anecdotes where necessary.</step5>
            <step6>Review the entire monologue to make sure it includes all the important information</step6>
            <step7>Don't include anything related to QR code or any link</step7>
            <step8>Return the script only. The response should start with the script and end with it</step8>
            <step9>Response should not contain anything like Script: and must be plain text no special characters. </step9>
        </prompt>
        """

    llm_prompt += f"\n\n<!-- Please make the script so that it {video_preference} the content. -->"

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


def generate_keywords(text: str):
    GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    llm_prompt = """
    Given the script, create a sequence of descriptive prompts for image generation that accurately reflect the key themes and concepts presented in the text.  The prompts must be in sequence with the script and must describe the text accurately. Each prompt should be vivid and evoke clear visual imagery, suitable for various artistic interpretations. Each prompt should contain only one phrase of max 10 words. The number of prompts should be flexible, depending on the richness of the text. As you progress through the document, provide each prompt in the order that corresponds with the content, ensuring that they collectively depict the narrative or themes in a cohesive manner. Output the prompts as a python list, ready for sequential use in a generative AI image generation API.
    """

    response = model.generate_content(llm_prompt + text)
    start_idx = response.text.find("[")
    end_idx = response.text.rfind("]") + 1
    trimmed_response = response.text[start_idx:end_idx]

    return ast.literal_eval(trimmed_response)


def generate_keywords_fast(text: str):
    GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    llm_prompt = """
    Given the extracted content from a document, generate 20 one or max three words keywords for use as prompts in image generation from the provided text. Each phrase should be vivid and descriptive, evoking clear visual imagery while avoiding any company names, trademarked terms, or specific generative AI model names. The phrases should be suitable for a variety of creative concepts and should inspire diverse artistic interpretations. Output should be a python list with no name just list
    """
    response = model.generate_content(llm_prompt + text)
    start_idx = response.text.find("[")
    end_idx = response.text.rfind("]") + 1
    trimmed_response = response.text[start_idx:end_idx]

    return ast.literal_eval(trimmed_response)


def get_prompts_from_script(script: str) -> List[str]:
    return [script]


def generate_answer_from_question(
    question: str = "What are the three states of matter?", speech: str = "formal"
):
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"""You are a school teacher. Your student asks you some questions, and you need to answer them in short and simple words. For example,
    if the student asks, "what are the three states of matter?", you should respond with The three states of matter are solid, liquid, and gas. 
    Solids have a fixed shape and volume, liquids take the shape of their container while maintaining a fixed volume, and gases fill the entire space available to them.

    Answer in {speech} speech?"

    User input is:
    My question is {question}

    Note: Do not include any markup like using * (asterisk) or any bullet points for formatting. Just plain text.
    """

    response = model.generate_content(prompt)

    return response.text

def get_loan_type(script):
    # Dictionary mapping loan types to their keywords
    loan_keywords = {
        "home_loan": ["home-loans", "mortgage"],
        "car_loan": ["auto-loans", "car-loans"],
        "personal_loan": ["personal-loans"],
        "health_insurance": ["health-insurance"],
        "life_insurance": ["life-insurance"],
    }
    
    # Counter to track occurrences of each loan type
    loan_counts = Counter()
    
    # Lowercase the script for case-insensitive matching
    script = script.lower()
    
    # Count occurrences of each keyword
    for loan_type, keywords in loan_keywords.items():
        for keyword in keywords:
            loan_counts[loan_type] += script.count(keyword)
    
    # Find the loan type with the most occurrences
    most_common_loan = loan_counts.most_common(1)
    return most_common_loan[0][0] if most_common_loan else None