import os
import uuid
import json
from datetime import datetime, timezone
from google import genai
from models import db, QCRecord


def analyze_media(file_path, api_key):
    """Encapsulates Gemini API interaction"""
    client = genai.Client(api_key=api_key)
    
    # Upload the file to Gemini
    uploaded_file = client.files.upload(file=file_path)
    
    # Wait for file to be ready
    import time
    while uploaded_file.state.name == "PROCESSING":
        time.sleep(2)
        uploaded_file = client.files.get(name=uploaded_file.name)
    
    if uploaded_file.state.name == "FAILED":
        raise Exception("File processing failed on Gemini side.")
        
    model = 'gemini-2.5-flash'
    prompt = """Act as a biologist specialized in microscopic analysis of seaweed and algae. Analyze this seaweed quality control image and extract the following information in JSON format:
    {
        "technician": "Reiss Jones",
        "contamination": "Yes or No, being Yes if there is visible contamination from other organisms. Only organisms that are not seaweed or algae should be considered contaminants.",
        "contaminant": "type of contaminant if contamination is Yes (bacteria, fungi, or microalgae), otherwise null",
        "qualityScoring": "score from 0-10 based on visual quality. If sample seems degraded, remove 5 from the score. If sample is contaminated, remove 5 from the score. Score should never be lower than 0",
        "developmentalStage": "one of: Spore Release, Germination, Zygote Formation, Juvenile Sporophyte Growth, Inconclusive",
        "biologicalSexRatio": "estimated ratio of male and female gametophytes (e.g., 30/70). The sum of the two numbers must be exactly 100. If not possible to identify, return null",
        "comment": "any additional comments or observations. It should not exceed 30 words"
    }
    
    Provide only the JSON object, no additional text."""

    safety_settings = [
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
    ]

    response = client.models.generate_content(
        model=model,
        contents=[prompt, uploaded_file],
        config={
            "temperature": 0.1,
            "safety_settings": safety_settings,
            "response_mime_type": "application/json"
        }
    )
    
    if not response.text:
        raise Exception("Gemini returned an empty response.")
        
    return response.text.strip()

def parse_analysis_json(response_text):
    """Extracts and validates JSON from Gemini output"""
    # 1. Try markdown code block extraction
    if '```' in response_text:
        try:
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0].strip()
            else:
                response_text = response_text.split('```')[1].split('```')[0].strip()
        except IndexError:
            pass # Fall back to brace searching
    
    # 2. Fallback: Search for the first { and last }
    if '{' in response_text and '}' in response_text:
        start_index = response_text.find('{')
        end_index = response_text.rfind('}')
        if start_index != -1 and end_index != -1:
            response_text = response_text[start_index:end_index+1]
    
    return json.loads(response_text)

