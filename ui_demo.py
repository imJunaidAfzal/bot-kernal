"""Driver program with sample UI."""

import gradio as gr
from chatbot import ChatBot, response_format
from generate_data import DataGenerator
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='logger.log',
                    filemode='w')  

logger = logging.getLogger(__name__)

file_handler = logging.FileHandler('logger.log')
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# DB setup
data_generator = DataGenerator()
data_generator.create_table()
data_generator.generate_records(num_records=10)

chat_agent = ChatBot()

def chat_wrapper(message):
    try:
        sql_statement = chat_agent.generate_sql(prompt=message)
        logger.info(sql_statement)
        response = chat_agent.execute_sql(sql=sql_statement)
        logger.info(response)

        response = response_format(f"User query: {message}\nRaw response: {response}\nGenerated response: ")

        return response
    except Exception as exp:
        return "Something went wront, please try again."

with gr.Blocks() as demo_ui:
    with gr.Row():
        gr.Markdown("<h1 align=center>Chatbot</h1>")
    with gr.Row():
        query = gr.Textbox(label="Query")
    with gr.Row():
        run_button = gr.Button("Run")
    with gr.Row():
        response = gr.Textbox(label="Response")
        run_button.click(fn=chat_wrapper, inputs=[query], outputs=[response])
    with gr.Row():
        gr.Markdown("<h1 align=center> DB Data</h1>")
    with gr.Row():
        table = gr.Dataframe(value=data_generator.get_data_as_dataframe())
    
demo_ui.launch()
