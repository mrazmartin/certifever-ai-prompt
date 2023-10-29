
import requests

DEFAULT_CONTEXT = ""

JSON_STYLE = """Provide the results in the following json format:
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
"""

class chatpdf_api:
    def __init__(self, key=None) -> None:

        self.debug_mode = False
        self.key = key
        self.context = DEFAULT_CONTEXT
        self.pdf_source_id = None

    def read_key_from_file(self, file_name="chatpdf_key.txt"):
        try:
            with open(file_name, 'r') as file:
                self.key = file.readline()
            if self.debug_mode:
                print(self.key)
        except:
            print("ERROR: key file doesnt exist")
    
    def upload_pdf(self, pdf_path):
        files = [('file', ('file', open(pdf_path, 'rb'), 'application/octet-stream'))]
        headers = {'x-api-key': self.key}

        response = requests.post(
            'https://api.chatpdf.com/v1/sources/add-file', headers=headers, files=files)
        
        if response.status_code == 200:
            print('Source ID:', response.json()['sourceId'])
        else:
            print('Status:', response.status_code)
            print('Error:', response.text)
        
        self.pdf_source_id = response.json()['sourceId']

    def debug(self, value=True):
        self.debug_mode =  value

    def create_prompt(self, question, rqst_sources=False):
        
        tmp_rqst = {"referenceSources": rqst_sources,
         "sourceId": tmp_api.pdf_source_id,
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

    def test_run(self):
        tmp_api.debug()
        tmp_api.read_key_from_file()
        tmp_api.upload_pdf("provided_file.pdf")
        print("\nPDF upload succ\n")
        
        topics = tmp_api.get_topics(5)
        
        question = f"Give me a question regarding the provided topics {topics} from the pdf file. {JSON_STYLE}."
        tmp_rqst = tmp_api.create_prompt(question, rqst_sources=True)

        tmp_api.ask_prompt(tmp_rqst)

tmp_api = chatpdf_api()
tmp_api.test_run()
