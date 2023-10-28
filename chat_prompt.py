# this is the best of Jason M. Mráz ever

# key: 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

import openai
import os
from dotenv import load_dotenv, find_dotenv

DEFAULT_CONTEXT = ""

class gpt_api:
    def __init__(self, key=None) -> None:
        self.model = "gpt-3.5-turbo"
        self.debug_mode = False
        if key:
            openai.api_key = key
        else:
            openai.api_key  = "forget about it"

        _ = load_dotenv(find_dotenv())

    def debug(self, value=True):
        self.debug_mode =  value

    def set_gpt_model(self, chat_model=None):
        if chat_model is None:
            print("\nNo model has been specified!\n")
            return
        self.model = chat_model

    def get_completion(self, prompt):
        messages = [{"role": "user", "content": prompt}]
        
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=0, # this is the degree of randomness of the model's output
        )

        return response.choices[0].message["content"]
    
    def prompt(self, context=DEFAULT_CONTEXT, text=None):

        if text is None:
            raise ValueError("No text has been provided, exiting")

        prompt = f"{context}{text}"
        response = get_completion(prompt)
        if self.debug_mode:
            print("\nquery:\n" + prompt + "\n" + "response:\n")
            print(response)
        return 



def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

###
tmp_api = gpt_api("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")
tmp_api.debug(True)
tmp_api.prompt(text="Give me two true or false coding question answer pairs based on python, return it in json format, keep the difficulty level on very hard, provide examples for each question")
"""
{
  "questions": [
    {
      "question": "True or False: In Python, the 'is' operator compares the values of two objects.",
      "answer": "False",
      "example": "x = [1, 2, 3]\ny = [1, 2, 3]\nprint(x is y)  # Output: False"
    },
    {
      "question": "True or False: Python supports tail call optimization (TCO) for recursive functions.",
      "answer": "False",
      "example": "import sys\nsys.setrecursionlimit(10**6)\n\ndef factorial(n, acc=1):\n    if n == 0:\n        return acc\n    return factorial(n-1, n*acc)\n\nprint(factorial(1000))  # Output: RecursionError: maximum recursion depth exceeded in comparison"
    }
  ]
}
"""
exit()
###

def main_test():
    print("\nReady to HACK!\n\n")
    _ = load_dotenv(find_dotenv())

    openai.api_key  = "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"

    text = f"""
    You should express what you want a model to do by \ 
    providing instructions that are as clear and \ 
    specific as you can possibly make them. \ 
    This will guide the model towards the desired output, \ 
    and reduce the chances of receiving irrelevant \ 
    or incorrect responses. Don't confuse writing a \ 
    clear prompt with writing a short prompt. \ 
    In many cases, longer prompts provide more clarity \ 
    and context for the model, which can lead to \ 
    more detailed and relevant outputs.
    """
    prompt = f"""
    Summarize the text delimited by triple backticks \ 
    into a single sentence.
    ```{text}```
    """
    response = get_completion(prompt)
    print(response)

