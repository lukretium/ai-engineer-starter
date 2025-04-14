import aiohttp

from app.llm.base import LLM

HTTP_OK = 200


class OllamaLLM(LLM):
    def __init__(
        self, model: str = "llama3.2", base_url: str = "http://localhost:11434"
    ):
        self.model = model
        self.base_url = base_url
        self.session: aiohttp.ClientSession | None = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def generate(self, prompt: str, context: list[str]) -> str:
        if not self.session:
            self.session = aiohttp.ClientSession()

        context_str = "\n\n".join(context)
        full_prompt = f"{context_str}\n\nQuestion: {prompt}\n\nAnswer:"

        async with self.session.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": full_prompt,
                "stream": False,
            },
        ) as response:
            if response.status != HTTP_OK:
                raise Exception(f"Ollama API error: {await response.text()}")
            result = await response.json()
            return result["response"]
