import gradio as gr

from app.core.config_manager import ConfigManager, LLMType, VectorStoreType
from app.db.postgres.session import get_db
from app.db.vector_store.factory import VectorStoreFactory
from app.embeddings.factory import EmbeddingFactory
from app.llm.factory import LLMFactory
from app.rag.simple_rag import SimpleRAG


def create_gradio_ui() -> gr.Blocks:
    with gr.Blocks() as demo:
        gr.Markdown("# AI Engineer Interface")

        with gr.Tab("RAG Chat"):
            with gr.Row():
                with gr.Column(scale=2):
                    chatbot = gr.Chatbot(height=500)
                    msg = gr.Textbox(label="Your message")
                    clear = gr.Button("Clear")
                with gr.Column(scale=1):
                    confidence_score = gr.Number(
                        label="Confidence Score", interactive=False
                    )
                    source_docs = gr.JSON(label="Source Documents")

            async def respond(
                message: str, chat_history: list[tuple[str, str]]
            ) -> tuple[str, list[tuple[str, str]], float, list[dict]]:
                async for db in get_db():
                    vector_store = VectorStoreFactory.create_vector_store(session=db)
                    llm = LLMFactory.create_llm()
                    embedding_provider = EmbeddingFactory.create_embedding_provider()
                    rag = SimpleRAG(vector_store, llm, embedding_provider)

                    response = await rag.query(message)
                    chat_history.append((message, response.answer))

                    # Convert documents to a format that can be displayed in JSON
                    docs_json = [
                        {
                            "content": doc.content,
                            "confidence": doc.metadata.get("confidence_score", 0.0),
                        }
                        for doc in response.documents
                    ]

                    return "", chat_history, response.confidence_score, docs_json

            msg.submit(
                respond, [msg, chatbot], [msg, chatbot, confidence_score, source_docs]
            )
            clear.click(
                lambda: ("", [], 0.0, []),
                None,
                [msg, chatbot, confidence_score, source_docs],
                queue=False,
            )

        with gr.Tab("Configuration"):
            with gr.Row():
                vector_store = gr.Dropdown(
                    choices=[t.value for t in VectorStoreType],
                    label="Vector Store",
                    value=ConfigManager.get_config().vector_store_type.value,
                )
                llm = gr.Dropdown(
                    choices=[t.value for t in LLMType],
                    label="LLM",
                    value=ConfigManager.get_config().llm_type.value,
                )

            def update_config(vector_store_type: str, llm_type: str) -> str:
                ConfigManager.update_from_ui(vector_store_type, llm_type)
                return "Configuration updated successfully!"

            update_btn = gr.Button("Update Configuration")
            output = gr.Textbox(label="Status")

            update_btn.click(update_config, inputs=[vector_store, llm], outputs=output)

        return demo
