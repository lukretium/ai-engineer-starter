from openai import AsyncOpenAI

from app.llm.base import LLM


class OpenAILLM(LLM):
    def __init__(self, api_key: str, model: str):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model

    async def generate(self, prompt: str, context: list[str]) -> str:
        context_str = "\n\n".join(context)
        full_prompt = f"{context_str}\n\nQuestion: {prompt}\n\nAnswer:"

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": full_prompt}],
            max_tokens=1024,
        )

        return str(response.choices[0].message.content)
