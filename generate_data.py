"""Script to generate the demo data and save in sql."""

import sqlite3
import random


class DataGenerator:
    """
    The TradeDataGenerator class manages the creation and 
    population of a SQLite 'trades' table with random trade records.
    """

    def __init__(self, db_name="trades.db"):

        self.db_name = db_name

    def create_table(self):
        """
        Create the 'trades' table in the SQLite database if it does not exist.

        This method establishes a connection to the SQLite database,
        creates a table named 'trades' with columns 'id', 'symbol', 'quantity', and 'price',
        and commits the changes.

        If the table already exists, this method does nothing.

        Returns:
        None
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL
            )
        ''')

        conn.commit()
        conn.close()

    def generate_records(self, num_records: int) -> None:
        """
        Generate and insert random trade records into the 'trades' table.

        This method generates a specified number of random trade records.

        Parameters:
        - num_records (int): The number of trade records to generate and insert.

        Returns:
        None
        """
        symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']

        records = []
        for _ in range(num_records):
            symbol = random.choice(symbols)
            quantity = random.randint(1, 100)
            price = round(random.uniform(50.0, 2000.0), 2)
            records.append((symbol, quantity, price))

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.executemany('''
            INSERT INTO trades (symbol, quantity, price)
            VALUES (?, ?, ?)
        ''', records)

        conn.commit()
        conn.close()

    def show_all_records(self):
        """
        Retrieve and display all records from the 'trades' table.

        Returns:
        None
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM trades')
        records = cursor.fetchall()

        conn.close()

        print("All Records in 'trades' table:")
        print(*records, sep="\n")

    def get_table_schema(self):
        """
        Retrieve the schema information for a given table in an SQLite database.

        This function connects to the specified SQLite database, executes a PRAGMA query
        to get the schema information for the specified table, and returns a list of tuples
        containing details about each column in the table.

        Parameters
        ----------
        table_name (str):
            The name of the table for which to retrieve the schema.

        db_name (str, optional):
            The name of the SQLite database. Default is "trades.db".

        Returns
        -------
        list of tuples:
            A list containing tuples with schema information for each column in the table.
        """

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("PRAGMA table_info(trades)")
        schema = cursor.fetchall()
        schema = [str(column_info) for column_info in schema]
        schema = "\n".join(schema)
        conn.close()
        return schema

# generator = DataGenerator()
# generator.create_table()
# generator.generate_records(10)
# # generator.show_all_records()

# schema = generator.get_table_schema()
# print("Table Schema for 'trades':")
# print(schema)
