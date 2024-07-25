from openai import OpenAI
import os
import sys

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

user_prompt = ''.join(sys.argv[1:])
model = "gpt-3.5-turbo"

response = client.chat.completions.create(
     model= model,
     messages=[
         {"role": "system", "content": ""},
         {"role": "user", "content": user_prompt}
     ],
     temperature=0.7,
     max_tokens=64,
     top_p=0
)
print(response.choices[0].message.content)
