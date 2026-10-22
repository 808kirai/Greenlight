import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  #this reads the.env file and loads the varianbles into the environment

client = OpenAI (base_url=os.environ["LLM_BASE_URL"], api_key=os.environ["LLM_API_KEY"])

#print every Nemotron model Nvidia offers
for m in client.models.list():
    if "nemotron" in m.id.lower():
        print(m.id)

#send one test message to the small, fast model
reply = client.chat.completions.create(
    model="nvidia/nemotron-3.5-lightning-30b-a3b",
    messages=[{"role": "user", "content": "In one sentence: what is a breaking change in a Python library?"}],
)
print(reply.choices[0].message.content)
