import os
import openai

openai.api_key = os.environ.get("OPENAI_API_KEY")

def translate_text(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a professional English translator for B2B communication in agriculture."},
            {"role": "user", "content": text}
        ],
        temperature=0.4
    )
    return response.choices[0].message["content"].strip()