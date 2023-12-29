"""
The ChatBot module enables SQL query generation and 
execution for trade records in SQLite based on user prompts.
"""

import os
import json
import sqlite3
from dotenv import load_dotenv
from openai import OpenAI

# env setup
load_dotenv()
API_KEY = os.getenv("API_KEY")
client = OpenAI(api_key=API_KEY)

current_path = os.path.dirname(__file__)


class ChatBot:
    """
    The ChatBot class manages SQL query generation and 
    execution for trade records in SQLite based on user prompts.
    """

    def __init__(self, db_name="trades.db"):

        self.db_name = db_name

    def generate_sql(self, prompt: str):
        """
        Generate an SQL statement based on the user prompt.

        This method generates a simple SQL SELECT statement from the user prompt.

        Parameters
        ----------
        prompt (str):
            The user input prompt.

        Returns
        -------
        str
            The generated SQL statement.
        """
        prompt_path = os.path.join(current_path, "prompts/generate_sql_query.json")
        PROMPT = json.loads(
            open(prompt_path, mode="r", encoding="utf-8").read()
        )
        system_prompt = PROMPT['PROMPT']
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                system_prompt,
                {
                "role": "user",
                "content": f"User query: {prompt}\nSQL query:"
                }
            ],
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            )
        response = response.choices[0].message.content

        return response

    def execute_sql(self, sql: str):
        """
        Execute an SQL statement and return the result.

        This method connects to the SQLite database, executes the provided SQL statement,
        fetches the result, and closes the connection.

        Parameters
        ----------
        sql (str): 
            The SQL statement to execute.

        Returns
        -------
        list:
            The result of the SQL query.
        """
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            cursor.execute(sql)
            response = cursor.fetchall()

            conn.close()
            return response
        except Exception as exp:
            return "Please try with other query."


class ChatAgent:
    """
    The ChatAgent class manages the interaction between the user and the chatbot.
    """

    def __init__(self) -> None:
        self.chatbot = ChatBot()
    
    def get_response(self, user_query: str):
        """
        Get a response from the chatbot based on the user query.

        This method generates an SQL query from the user query, executes the query,
        and returns the result.

        Parameters
        ----------
        user_query (str):
            The user query.

        Returns
        -------
        list:
            The result of the SQL query.
        """
        sql = self.chatbot.generate_sql(user_query)
        response = self.chatbot.execute_sql(sql)
        return response

def response_format(prompt):
    """
    Generate a response based on the query and raw response.

    Parameters
    ----------
    prompt (str):
        Prompt with query and raw answer.

    Returns
    -------
    str:
        The generated response.
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You're response builder. Generate the response for the user based on the query and raw answer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=256,
        top_p=1,
    )
    response = response.choices[0].message.content
    return response
