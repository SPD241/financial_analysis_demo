import google.generativeai as genai
from constants import API_KEY
import os
import numpy as np

class Generative_Model:
    def __init__(self):
        api_key = os.gotenv("GOOGLE_API_KEY")
        if not api_key:
            raise RuntimeError("GOOGLE_API_KEY environment variable is not set")
        
        genai.configure(api_key=api_key)

        

    def chat( prompt:str) -> str:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        return response.text

def prompt (rsi_last, macd_last, signal_last) -> str:
    

    prompt = f""" You are an expert financial market assistant. Check up the indicators bellow and make a suggestion about it.

    Indicators: 
    - RSI(period = 14): {rsi_last:.2f}
    - MACD: {macd_last:.2f}
    - MACD Signal: {signal_last:.2f}

    Rules: 
    - Do NOT give financial advice
    - Explain the technical situation clearly
    - Mention risks and momentum
    - don't extend more than 200 words 

    Explain the current market state and make a suggeston about the following movement
    """
    return prompt