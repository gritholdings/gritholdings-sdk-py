import json
import openai
import os


class OpenaiAdapter:
    """Openai Adapter"""
    def __init__(self):
        self.openai = openai
        self.openai.api_key = os.environ.get("OPENAI_API_KEY")
        self.openai.organization = os.environ.get("OPENAI_ORGANIZATION_ID")

    def chat(self, messages, temperature=1):
        completion = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=messages,
            temperature=temperature,
        )
        return completion.choices[0].message

    def chat_no_timeout(self, messages, temperature=1):
        completion = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=messages,
            temperature=temperature,
        )
        return completion.choices[0].message

    def create(self, text):
        response = openai.Completion.create(
            model="gpt-4-turbo",
            prompt=text,
            max_tokens=100,
            temperature=1,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        return response.choices[0].text


class LLM:
    def __init__(self):
        self.openai_adapter = OpenaiAdapter()

    def chat(self, messages, temperature=1):
        return self.openai_adapter.chat(messages, temperature)

    def chat_no_timeout(self, messages, temperature=1):
        return self.openai_adapter.chat_no_timeout(messages, temperature)

    def create(self, text):
        return self.openai_adapter.create(text)