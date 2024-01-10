import os
import arrow
from dotenv import load_dotenv
import openai

load_dotenv()

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

openai.api_key = os.getenv('OPENAI_KEY')

def ask_gpt(system_prompt, user_prompt, temp=0.1, model='gpt-4'):
    print('\n\n---------------- QUERYING CHATGPT ----------------')
    system = {'role': 'system', 'content': system_prompt}
    user = {'role': 'user', 'content': user_prompt}
    completion = openai.ChatCompletion.create(model=model, messages=[system, user], temperature=temp)
    return completion.choices[0].message.content

def save_response(resp: str, symbol: str):
    date = arrow.now(tz='America/New_York').format('YYYY_MM_DD')
    report_path = os.path.join(PROJECT_ROOT, 'reports', date)
    os.makedirs(report_path, exist_ok=True)

    fp = os.path.join(report_path, symbol + '.md')
    with open(fp, 'w') as f:
        f.write(resp)

    print(resp)