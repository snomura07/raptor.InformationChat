import os
import time
from openai import OpenAI

class Assistant():
    TERMINAL_STATES = [
        "expired",
        "completed",
        "failed",
        "incomplete",
        "cancelled",
    ]

    def __init__(self):
        self.client = OpenAI()
        self.assistantId = os.getenv('OPENAI_ASSISTANT_ID')
        self.debugMode   = os.getenv('OPENAI_DEBUG_MODE', 'false').lower() == 'true'
        self.thread      = self.client.beta.threads.create()

    def createAndPoll(self, message) -> str:
        if self.debugMode:
            print("OpenAI Assistant API : debug mode now")
            return '{"main_command":"hello","optional_value":[], "optional_string:[]"}'

        # Messageの作成
        self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=message,
        )

        # Assistantの実行
        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=self.thread.id,
            assistant_id=self.assistantId,
            truncation_strategy={
                "type": "last_messages",
                "last_messages": 10
            },
        )

        retrievedRun = self.client.beta.threads.runs.retrieve(
            thread_id=self.thread.id,
            run_id=run.id
        )

        if retrievedRun.status in self.TERMINAL_STATES:
            messages = self.client.beta.threads.messages.list(thread_id=self.thread.id)
            assistantRes = messages.data[0].content[0].text.value
            print(f"Assistant status: {retrievedRun.status} , res: {assistantRes}")
            return assistantRes


if __name__ == "__main__":
    assistant = Assistant()
    assistant.createAndPoll('hi')
    time.sleep(1)
    assistant.createAndPoll('MasterConfigを取得して')
