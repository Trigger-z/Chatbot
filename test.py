from openai import OpenAI
import os
from dotenv import load_dotenv

api_key = os.getenv("API_KEY_TEST")
client = OpenAI(api_key=api_key)

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  messages=[
    {"role": "user", "content": "write a haiku about ai"}
  ]
)

print(completion.choices[0].message);