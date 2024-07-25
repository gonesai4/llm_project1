import uvicorn

import config
import os
from openai import OpenAI
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

app = FastAPI()

# get, post, put, delete

class Body(BaseModel):
    text: str

@app.get("/")
def welcome():
    return {"Hello": "World"}

@app.post("/response")
def generate(body: Body):
    prompt = body.text  # user prompt
    assistant = config.assistant_id
    assistant = client.beta.assistants.create(
        name="Profile Assistant",
        instructions="You are profile master who is having 10 years of experience. Write summary of this profile reading from pdf file ",
        model="gpt-3.5-turbo",
        tools=[{"type": "file_search"}],
    )

    # Create a vector store called "Financial Statements"
    vector_store = client.beta.vector_stores.create(name="Profile Management")

    # Ready the files for upload to OpenAI
    file_paths = ["Mahesh_Resume-Final.pdf"]
    file_streams = [open(path, "rb") for path in file_paths]

    # Use the upload and poll SDK helper to upload the files, add them to the vector store,
    # and poll the status of the file batch for completion.
    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id, files=file_streams
    )

    assistant = client.beta.assistants.update(
        assistant_id=config.assistant_id,
        tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
    )

    # Upload the user provided file to OpenAI
    message_file = client.files.create(
        file=open("Mahesh_Resume-Final.pdf", "rb"), purpose="assistants"
    )

    # Create a thread and attach the file to the message
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": "write summary of the profile reading from pdf file",
                # Attach the new file to the message.
                "attachments": [
                    {"file_id": message_file.id, "tools": [{"type": "file_search"}]}
                ],
            }
        ]
    )

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=config.assistant_id,
        instructions="Please address the user as Client. The user has a premium account."
    )

    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        text = ""
        if run.status == "completed":
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            latest_message = messages.data[0]
            text = latest_message.content[0].text.value
            print(text)
            break
    return text

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
