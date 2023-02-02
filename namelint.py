import os
import openai
from dotenv import load_dotenv

class NameLint:
    def __init__(self, title):
        self.title = title

    def lint(self):
        load_dotenv()

        print(self.title)

        openai.api_key = os.getenv("OPENAI_API_KEY")

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt="Identifiziere den Produktnamen aus diesem Titel: " + self.title,
            temperature=0,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

            
        return(response['choices'][0]['text'].replace('\n', ''))