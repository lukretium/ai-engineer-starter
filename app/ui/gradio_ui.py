import gradio as gr
from fastapi import FastAPI

from app.core.config_manager import ConfigManager, LLMType, VectorStoreType


def create_gradio_ui(app: FastAPI) -> None:
    with gr.Blocks() as demo:
        gr.Markdown("# AI Engineer Configuration")

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

    app.mount("/ui", demo)
