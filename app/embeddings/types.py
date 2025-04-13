from enum import Enum


class EmbeddingType(str, Enum):
    OPENAI = "openai"
    HUGGINGFACE = "huggingface"
    OLLAMA = "ollama"
