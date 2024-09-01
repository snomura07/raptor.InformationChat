import os
import time
from openai import OpenAI

TERMINAL_STATES = [
    "expired",
    "completed",
    "failed",
    "incomplete",
    "cancelled",
]

os.environ["OPENAI_API_KEY"] = ""
client = OpenAI()

assistant_id = 'asst_pjVna6SM5YZNr9uSExGqWBny'
print(f'assistant_id:{assistant_id}')

# Threadの作成
empty_thread = client.beta.threads.create()
thread_id = empty_thread.id
print(thread_id)

# Messageの作成
client.beta.threads.messages.create(
    thread_id=thread_id,
    role="user",
    content="No18ピンをINPUTに",
)

# Assistantの実行
run = client.beta.threads.runs.create_and_poll(
    thread_id=thread_id,
    assistant_id=assistant_id,
    truncation_strategy={
        "type": "last_messages",
        "last_messages": 10
    },
)
print(f"Created run with ID: {run.id}")

retrieved_run = client.beta.threads.runs.retrieve(
    thread_id=thread_id,
    run_id=run.id
)
print(retrieved_run.status)

if retrieved_run.status in TERMINAL_STATES:
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    assistant_response = messages.data[0].content[0].text.value
    print(f"Assistant response: {assistant_response}")
