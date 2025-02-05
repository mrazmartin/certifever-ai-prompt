import os
import requests
from chat_prompt import gpt_api

DEFAULT_CONTEXT = ""

JSON_STYLE = """Put everything in json. Provide the results in the following json format:
    {
    "question": "What is the key difference between Python 2 and Python 3?",
    "options": [
        "AAA",
        "BBB",
        "CCC",
        "DDD"
      ],
    "correct_answer_id": 2,
    "explanation": short explanation of the correct answer in one short sentence,
    "topic":
    }
"""

class chatpdf_api:
    def __init__(self, key=None, pdf_path="", key_path="") -> None:

        self.debug_mode = False
        if key is None:
            self.key = self.read_key_from_file(key_path)
        else:
            self.key = key 
        self.context = DEFAULT_CONTEXT
        self.pdf_source_id = self.upload_pdf(pdf_path)
        print(self.pdf_source_id)

    def read_key_from_file(self, file_name=""):
        try:
            with open(file_name, 'r') as file:
                if self.debug_mode:
                    print(self.key)
                return file.readline()
        except:
            print("ERROR: key file doesnt exist")
    
    def upload_pdf(self, pdf_path):

        if not os.path.isfile(pdf_path):
            raise ValueError("No pdf to be uploaded!")

        files = [('file', ('file', open(pdf_path, 'rb'), 'application/octet-stream'))]
        headers = {'x-api-key': self.key}

        response = requests.post(
            'https://api.chatpdf.com/v1/sources/add-file', headers=headers, files=files)
        
        if response.status_code == 200:
            if self.debug:
                print('Source ID:', response.json()['sourceId'])
            return response.json()['sourceId']
        else:
            print('Status:', response.status_code)
            print('Error:', response.text)
            exit()

    def debug(self, value=True):
        self.debug_mode =  value

    def create_prompt(self, question, rqst_sources=False):
        
        tmp_rqst = {"referenceSources": rqst_sources,
         "sourceId": self.pdf_source_id,
         "messages": [
            {
            "role": "user",
            "content": f"{question}"
            }]
        }
        return tmp_rqst

    def get_topics(self, max_topics=3):

        new_promt = f"""Given the pdf file, select up to {max_topics} different topics.
        These topics will be later used to learn about the provided pdf.
        The reply formating should be [topic 1, topic 2, ..., topic 5]."""

        tmp_prompt = self.create_prompt(new_promt)
        tmp_result = self.ask_prompt(tmp_prompt)

        return tmp_result.json()['content']

    def ask_prompt(self, query=None):
        headers = {'x-api-key': self.key, "Content-Type": "application/json",}
        response = requests.post(
            'https://api.chatpdf.com/v1/chats/message', headers=headers, json=query)

        if response.status_code == 200:
            print('Result:', response.json()['content'])
            if "refererces" in response.json():
                print('References', response.json()['references'])
        else:
            print('Status:', response.status_code)
            print('Error:', response.text)
        
        return response

    def generate_reinforce(self, ):
        pass

    def test_run(self):
        self.debug()
        #tmp_api.upload_pdf("provided_file.pdf")
        
        if self.debug:
            print("Start: get topics")
        topics = self.get_topics(5)
        
        question = f"Give me a multiple choice question regarding the provided topics {topics} from the pdf file. {JSON_STYLE}."
        tmp_rqst = self.create_prompt(question, rqst_sources=True)

        self.ask_prompt(tmp_rqst)

class any_api():
    def __init__(self, api_service=None) -> None:
        self.service = api_service
        self.key = None

    def read_key(self, path):
        try:
            with open(path, 'r') as file:
                return file.readline()
        except:
            print("ERROR: key file doesnt exist")

    def init_question(self, profile, pdf_path, opt_context, key_path=""):
        
        self.key = self.read_key(key_path)
        
        if os.path.isfile(pdf_path):
            self.service = chatpdf_api(pdf_path=pdf_path, key=self.key)
        else:
            self.service = gpt_api(self.key)

        topics = self.service.get_topics(5)

        question = profile + f"Give me a multiple choice question regarding the provided topics {topics} from the pdf file." + JSON_STYLE
        tmp_query = self.service.create_prompt(question)
        response = self.service.ask_prompt(tmp_query)

        return {"topics": topics,
                "response": response}
    
    def reinfoce_topic(self, topic=""):
        # generate more questions about a given topic
        pass    
    
    def reinfoce_auto(self):
        # generate more questions by default
        raise NotImplemented
    
    def adjust_difficulty_topic(topics):
        raise NotImplemented
    
    def keep_going():
        raise NotImplemented

# tmp_api = chatpdf_api(pdf_path="provided_file.pdf", key_path="chatpdf_key.txt")
# tmp_api.test_run()

# comes from front end
profile_background = "junior developer"
profile_aim = "learn python" 
profile = f"I am a {profile_background}. I want to {profile_aim}"
pdf = "provided_file.pdf"
opt_context = ""  

# run question creator
our_api = any_api()
our_api.init_question(profile=profile, pdf_path=pdf, opt_context=opt_context, key_path="chatpdf_key.txt")