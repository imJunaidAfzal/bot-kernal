"""Driver program with sample UI."""

import gradio as gr
from chatbot import ChatBot
from generate_data import DataGenerator

# DB setup
data_generator = DataGenerator()
data_generator.create_table()
data_generator.generate_records(num_records=10)

chat_agent = ChatBot()

def chat_wrapper(message, chat_history):
    
    
    print(chat_history)

    return "message"

demo = gr.ChatInterface(fn=respond, title="Chatbot")
demo.launch()