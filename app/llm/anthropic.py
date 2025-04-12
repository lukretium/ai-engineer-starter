import anthropic
from anthropic.types import Message

from app.llm.base import LLM


class AnthropicLLM(LLM):
    def __init__(self, api_key: str, model: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    async def generate(self, prompt: str, context: list[str]) -> str:
        context_str = "\n\n".join(context)
        full_prompt = f"{context_str}\n\nQuestion: {prompt}\n\nAnswer:"

        response: Message = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{"role": "user", "content": full_prompt}],
        )

        return str(response.content[0].text)
