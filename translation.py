"""

This module contains the translation class.

"""

# Import from standard library
import logging


# Import from 3rd party libraries
import streamlit as st
from deep_translator import GoogleTranslator


class Translator:
    
    def __init__(self, ):
        pass

    @staticmethod
    def translate(prompt, target):
        
        """
        Call Google Translator with text prompt.
        Args:
            prompt: text prompt
            target: target language
        Return: translated text
        """

        try:
            translator = GoogleTranslator(source='auto', target=target)
            t = translator.translate(prompt)
            return t

        except Exception as e:
            logging.error(f"Google Translator API error: {e}")
            st.session_state.text_error = f"Google Translator API error: {e}"
            print("Error:", e)
        

# Usage:

# translator = Translator()
# a = translator.translate("Ko'chada ketayotgan yolg'iz chol", 'ko')
# print(a)