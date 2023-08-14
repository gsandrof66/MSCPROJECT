import openai
import configparser


class OPENAI():
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("Openai/oaiconf")
        openai.api_key = config.get("conn", "OPENAI_API_KEY")
    
    def get_completion(self, prompt, model="gpt-3.5-turbo"):
        messages = [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0, # this is the degree of randomness of the model's output
        )
        return response.choices[0].message["content"]
    
    def get_comp(self, text):
        prompt = f"""Summarize the text delimited by triple backticks in terms of accessibility 
        into a single sentence with no more than 20 words.```{text}```"""
        messages = [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0, # this is the degree of randomness of the model's output
        )
        return response.choices[0].message["content"]
    