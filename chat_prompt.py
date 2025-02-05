# this is the best of Jason M. Mráz ever

# key: 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

import openai
import os
from dotenv import load_dotenv, find_dotenv

DEFAULT_CONTEXT = ""

JSON_STYLE = """Provide the results in the following json format:
    "question": "What is the key difference between Python 2 and Python 3?",
    "options": [
        "AAA",
        "BBB",
        "CCC",
        "DDD"
      ],
    "correct_answer": 2,
    "explanation": short explanation of the correct answer 
"""

class gpt_api:
    def __init__(self, key=None) -> None:
        self.model = "gpt-3.5-turbo"
        self.debug_mode = False
        self.context = DEFAULT_CONTEXT

        if key:
            self.key = key

        # _ = load_dotenv(find_dotenv())

    def read_key_from_file(self, file_name="api_key.txt"):
        with open(file_name, 'r') as file:
            self.key = file.readline()

    def json_style(self, style=""):
        self.context = self.context + style

    def debug(self, value=True):
        self.debug_mode =  value

    def set_gpt_model(self, chat_model=None):
        if chat_model is None:
            print("\nNo model has been specified!\n")
            return
        self.model = chat_model

    def get_completion(self, prompt):
        messages = [{"role": "user", "content": prompt}]

        openai.api_key = self.key
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=0, # this is the degree of randomness of the model's output
        )

        return response.choices[0].message["content"]
    
    def prompt(self, text=None):

        if text is None:
            raise ValueError("No text has been provided, exiting")

        prompt = f"{self.context}{text}"
        response = self.get_completion(prompt)
        if self.debug_mode:
            print("\nquery:\n" + prompt + "\n" + "response:\n")
            print(response)
        return 



### example run

def example_run():
    tmp_api = gpt_api("catch me if you can")
    tmp_api.read_key_from_file("api_key.txt")
    tmp_api.debug(True)
    tmp_api.json_style(JSON_STYLE)
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

# example_run()