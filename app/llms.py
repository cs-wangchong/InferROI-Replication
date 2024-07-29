from abc import ABC, abstractmethod
import logging

from anthropic import Anthropic
from openai import OpenAI
import transformers
import torch


OPENAI_KEY = "YOUR KEY"
ANTHROPIC_KEY = "YOUR KEY"
HUGGINGFACE_KEY = "YOUR KEY"

LLM_FACTORY = {
    "gpt-3.5-turbo": lambda: ChatGPT("gpt-3.5-turbo"),
    "gpt-4-turbo": lambda: ChatGPT("gpt-4-turbo"),
    "gpt-4": lambda: ChatGPT("gpt-4"),
    "gpt-4o": lambda: ChatGPT("gpt-4o"),
    "claude-3.5": lambda: Claude("claude-3-5-sonnet-20240620"),
    "llama-3-8b": lambda: HuggingFace("meta-llama/Meta-Llama-3-8B-Instruct"),
    "gemma-2-9b": lambda: HuggingFace("google/gemma-2-9b-it"),
}


class LLM(ABC):
    def __init__(self, name, max_len=1024):
        self.name = name
        self.max_len = max_len

    @abstractmethod
    def query(self, question: str) -> str:
        raise NotImplementedError


class ChatGPT(LLM):
    PRICES = {
        "gpt-3.5-turbo": (0.5 / 1E6, 1.5 / 1E6),
        "gpt-4": (30 / 1E6, 60 / 1E6),
        "gpt-4-turbo": (10 / 1E6, 30 / 1E6),
        "gpt-4o": (5 / 1E6, 15 / 1E6),
    }
    TOTAL_COST = 0
    def __init__(self, name, max_len=1024):
        assert name in {"gpt-3.5-turbo", "gpt-4", "gpt-4-turbo", "gpt-4o"}, "unsupported ChatGPT version"
        super().__init__(name, max_len=max_len)
        self.client = OpenAI(api_key=OPENAI_KEY)

    def query(self, question: str) -> str:
        response = self.client.chat.completions.create(
            model=self.name,
            temperature=0,
            top_p=0,
            max_tokens=self.max_len,
            messages=[
                {
                    "role": "user",
                    "content": question
                }
            ],
        )
        answer = response.choices[0].message.content
        input_tokens, output_tokens = response.usage.prompt_tokens, response.usage.completion_tokens
        cost = ChatGPT.PRICES[self.name][0] * input_tokens + ChatGPT.PRICES[self.name][1] * output_tokens
        self.TOTAL_COST += cost
        logging.info(f"===== USAGE =====")
        logging.info(f"input tokens: {input_tokens}; output tokens: {output_tokens}")
        logging.info(f"query cost: ${round(cost, 4)}; total cost: ${round(self.TOTAL_COST, 4)}")
        logging.info(f"===== USAGE =====")
        return answer
    

class Claude(LLM):
    def __init__(self, name:str, max_len=1024):
        assert name.startswith("claude"), "unsupported Claude version"
        super().__init__(name, max_len=max_len)
        self.client = Anthropic(api_key=ANTHROPIC_KEY)

    def query(self, question: str) -> str:
        message = self.client.messages.create(
            model=self.name,
            max_tokens=self.max_len,
            temperature=0,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": question
                        }
                    ]
                }
            ]
        )
        return message.content



class HuggingFace(LLM):
    def __init__(self, name, max_len=1024):
        super().__init__(name, max_len=max_len)
        self.pipeline = transformers.pipeline(
            "text-generation",
            model=name,
            model_kwargs={"torch_dtype": torch.bfloat16},
            device_map="auto",
            token=HUGGINGFACE_KEY
        )


    def query(self, question: str) -> str:
        messages = [
            {"role": "user", "content": question},
        ]

        terminators = [
            self.pipeline.tokenizer.eos_token_id,
            self.pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")
        ]
        outputs = self.pipeline(
            messages,
            max_new_tokens=self.max_len,
            eos_token_id=terminators,
        )
        return outputs[0]["generated_text"][-1]["content"]
