from openai import OpenAI
import os
import anthropic
import re


ANTHROPIC_MODEL_NAME = "claude-3-opus-20240229"


class OpenaiAdapter:
    """Openai Adapter"""
    def __init__(self):
        # it will access the API key from os.environ
        self.client = OpenAI()

    def chat(self, messages, temperature=1):
        # Ensure messages is a list of message dictionaries
        formatted_messages = [
            {"role": "system", "content": message} if isinstance(message, str) else message
            for message in messages
        ]
        completion = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=formatted_messages,
            temperature=temperature,
        )
        return completion.choices[0].message


class AnthropicAdapter:
    """Anthropic Adapter"""
    def __init__(self):
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        self.client = anthropic.Anthropic(api_key=api_key)
        self.grader = Grader()

    def create(self, text):
        message = self.client.messages.create(
            model=ANTHROPIC_MODEL_NAME,
            max_tokens=1000,
            temperature=0.0,
            system="You are a useful assistant.",
            messages=[
                {"role": "user", "content": text}
            ]
        )
        return message.content[0].text

    def grade_completion(self, output, golden_answer):
        messages = self.grader.build_grader_prompt(output, golden_answer)
        completion = self.create(messages)
        # Extract just the label from the completion (we don't care about the thinking)
        pattern = r'<correctness>(.*?)</correctness>'
        match = re.search(pattern, completion, re.DOTALL)
        if match:
            return match.group(1).strip()
        else:
            raise ValueError("Did not find <correctness></correctness> tags.")


class Grader:
    """Model-based Grading"""
    def __init__(self):
        pass

    def build_grader_prompt(self, answer, rubric):
        """We start by defining a "grader prompt" template."""
        user_content = f"""You will be provided an answer that an assistant gave to a question, and a rubric that instructs you on what makes the answer correct or incorrect.
        
        Here is the answer that the assistant gave to the question.
        <answer>{answer}</answer>
        
        Here is the rubric on what makes the answer correct or incorrect.
        <rubric>{rubric}</rubric>
        
        An answer is correct if it entirely meets the rubric criteria, and is otherwise incorrect. =
        First, think through whether the answer is correct or incorrect based on the rubric inside <thinking></thinking> tags. """
        f"""Then, output either 'correct' if the answer is correct or 'incorrect' if the answer is incorrect inside <correctness></correctness> tags."""

        messages = [{'role': 'user', 'content': user_content}]
        return messages

    def evaluate(self, prompt, completion):
        pass


class LLM:
    def __init__(self, adapter_type):
        if adapter_type == "openai":
            self.adapter = OpenaiAdapter()
        elif adapter_type == "anthropic":
            self.adapter = AnthropicAdapter()
        else:
            raise ValueError(f"Unsupported adapter type: {adapter_type}")