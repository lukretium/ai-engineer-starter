import gradio as gr

from app.core.config_manager import ConfigManager, LLMType, VectorStoreType
from app.llm.factory import LLMFactory


def create_gradio_ui() -> gr.Blocks:
    with gr.Blocks() as demo:
        gr.Markdown("# AI Engineer Interface")

        with gr.Tab("Chat"):
            chatbot = gr.Chatbot(height=500)
            msg = gr.Textbox(label="Your message")
            clear = gr.Button("Clear")

            async def respond(message, chat_history):
                llm_instance = LLMFactory.create_llm()
                response = await llm_instance.generate(message, [])
                chat_history.append((message, response))
                return "", chat_history

            msg.submit(respond, [msg, chatbot], [msg, chatbot])
            clear.click(lambda: None, None, chatbot, queue=False)

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
