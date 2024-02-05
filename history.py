import sqlite3
import threading

class DatabaseHandler:
    def __init__(self, db_file='history.db'):
        self.db_file = db_file
        self.lock = threading.Lock()

    def connect(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        return conn, cursor

    def create_table(self):
        
        with self.lock:
            conn, cursor = self.connect()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY,
                    input TEXT NOT NULL,
                    output TEXT NOT NULL
                )
            ''')
            conn.commit()
            conn.close()

    def insert_data(self, input_data, output_data):
        if input_data is not None and output_data is not None:
            with self.lock:
                conn, cursor = self.connect()
                cursor.execute("INSERT INTO history (input, output) VALUES (?, ?)", (input_data, output_data))
                conn.commit()
                conn.close()
        else:
            print("Error: Both input_data and output_data must be provided.")

    def fetch_all_data(self):
        with self.lock:
            conn, cursor = self.connect()
            cursor.execute("SELECT * FROM history")
            columns = [column[0] for column in cursor.description]
            data = [dict(zip(columns, row)) for row in cursor.fetchall()]
            conn.close()
            return data

if __name__ == "__main__":
    db_handler = DatabaseHandler()

    db_handler.create_table()
    db_handler.insert_data('sample code', 'this code')
    data = db_handler.fetch_all_data()
    print("All data:", data)
