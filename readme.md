# SQL Chatbot

This is a simple chatbot that can generate SQL queries from natural language prompts and fetch results from a SQLite database.

## Features

- Generates SQL queries from natural language prompts.
- Executes SQL queries against a SQLite database 
- Returns query results to the user
- Includes sample UI built with Gradio for demo

## Usage

### Setup

1. **Clone this repo**
    ```bash
    git clone https://github.com/imJunaidAfzal/bot-kernal.git
    ```
2. **Move to project directory**

    ```bash
    cd bot-kernal
    ```
3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set OpenAI API key**

   - Create a `.env` file in project root with your OpenAI key as `API_KEY`.

5. **Start UI**

   ```bash
   python ui_demo.py
   ```

### **Development**

- `chatbot.py` - Main chatbot logic
- `generate_data.py` - Script to generate sample data
- `ui_demo.py` - Gradio UI 

**This project is developed and tested with Python 3.11**