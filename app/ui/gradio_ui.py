import json

import gradio as gr

from app.core.config_manager import ConfigManager, LLMType, VectorStoreType
from app.db.postgres.session import get_db
from app.db.vector_store.factory import VectorStoreFactory
from app.embeddings.factory import EmbeddingFactory
from app.embeddings.types import EmbeddingType
from app.llm.factory import LLMFactory
from app.rag.simple_rag import SimpleRAG
from app.schemas.rag import DocumentCreate


def create_gradio_ui() -> gr.Blocks:  # noqa: PLR0915
    with gr.Blocks() as demo:
        gr.Markdown("# AI Engineer Interface")

        with gr.Tab("RAG Chat"):
            with gr.Row():
                with gr.Column(scale=2):
                    gr.Markdown("### Active Models")
                    active_models = gr.Textbox(
                        value=f"LLM: {ConfigManager.get_config().llm_type.value}\n"
                        f"Embedding: {ConfigManager.get_config().embedding_type.value}",
                        label="Active Models",
                        interactive=False,
                    )
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

        with gr.Tab("Model Experimentation"):
            with gr.Row():
                with gr.Column():
                    embedding_model = gr.Dropdown(
                        choices=[t.value for t in EmbeddingType],
                        label="Embedding Model",
                        value=ConfigManager.get_config().embedding_type.value,
                    )
                    llm_model = gr.Dropdown(
                        choices=[t.value for t in LLMType],
                        label="LLM Model",
                        value=ConfigManager.get_config().llm_type.value,
                    )
                    vector_store = gr.Dropdown(
                        choices=[t.value for t in VectorStoreType],
                        label="Vector Store",
                        value=ConfigManager.get_config().vector_store_type.value,
                    )
                    update_models = gr.Button("Update Models")
                    model_status = gr.Textbox(label="Status", interactive=False)

            def update_model_config(
                embedding_type: str, llm_type: str, vector_store_type: str
            ) -> tuple[str, str]:
                ConfigManager.update_from_ui(
                    vector_store_type, llm_type, embedding_type
                )
                model_info = f"LLM: {llm_type}\nEmbedding: {embedding_type}"
                return "Model configuration updated successfully!", model_info

            update_models.click(
                update_model_config,
                inputs=[embedding_model, llm_model, vector_store],
                outputs=[model_status, active_models],
            )

        with gr.Tab("Data Import"):
            with gr.Row():
                with gr.Column():
                    json_input = gr.Textbox(
                        label="JSON Data",
                        placeholder="Paste your JSON data here",
                        lines=10,
                    )
                    import_btn = gr.Button("Import Data")
                    import_status = gr.Textbox(label="Import Status", interactive=False)

            async def import_data(json_data: str) -> str:
                try:
                    data = json.loads(json_data)
                    if "documents" not in data:
                        return "Error: JSON must contain a 'documents' array"

                    # Convert JSON documents to DocumentCreate objects
                    documents = [
                        DocumentCreate(
                            content=doc["content"],
                            metadata=doc.get("metadata", {}),
                        )
                        for doc in data["documents"]
                    ]

                    async for db in get_db():
                        vector_store = VectorStoreFactory.create_vector_store(
                            session=db
                        )
                        llm = LLMFactory.create_llm()
                        embedding_provider = (
                            EmbeddingFactory.create_embedding_provider()
                        )
                        rag = SimpleRAG(vector_store, llm, embedding_provider)

                        await rag.add_documents(documents)
                        return f"Successfully imported {len(documents)} documents"
                except json.JSONDecodeError:
                    return "Error: Invalid JSON format"
                except KeyError as e:
                    return f"Error: Missing required field in document: {e!s}"
                except Exception as e:
                    return f"Error: {e!s}"

            import_btn.click(
                import_data,
                inputs=[json_input],
                outputs=import_status,
            )

        return demo
