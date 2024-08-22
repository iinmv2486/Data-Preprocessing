from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are helpful assitant."},
        {
            "role": "user",
            "content": "Say this is a test"
        }
    ]
)

print(completion.choices[0].message["content"])