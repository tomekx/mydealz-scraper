import os
import openai
from dotenv import load_dotenv

from logger import get_module_logger

# request GPT-3 to extract product name from deal title
def lint(title):
    load_dotenv()

    openai.api_key = os.getenv("OPENAI_API_KEY")

    try:

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt="Identifiziere den Produktnamen aus diesem Titel und füge keine neuen Wörter hinzu: " + title,
            temperature=0,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

    except:
        get_module_logger('namelint').info(f'Error occured in namelint on deal {title}')
        
    return(response['choices'][0]['text'].replace('\n', ''))