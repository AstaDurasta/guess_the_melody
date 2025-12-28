import sqlite3

MAX_VALUE_INDEX = 0

class Database:

    def __init__(self, database_name):
        self.database_name = database_name
    
    def create_table(self, table_name, fields):
        query = self.get_query_to_create_table(table_name, fields)
        self.run_database_query(query)

    def get_query_to_create_table(self, table_name, fields):
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({fields})"
        return query
    
    def run_database_query(self, query):
        self.connect()
        self.execute_request(query)
        self.finish_transaction()
    
    def connect(self):
        self.connect_to_database()
        self.create_cursor()

    def connect_to_database(self):
        self.connection = sqlite3.connect(self.database_name)

    def create_cursor(self):
        self.cursor = self.connection.cursor()
    
    def execute_request(self, query):
        self.cursor.execute(query)

    def finish_transaction(self):
        self.commit()
        self.close()
    
    def commit(self):
        self.connection.commit()
    
    def close(self):
        self.connection.close()

    def add_row_to_table(self, table_name, fields, values):
        query = self.get_query_to_add_new_row(table_name, fields, values)
        self.run_database_query(query)

    def get_query_to_add_new_row(self, table_name, fields, values):
        query = f"INSERT OR IGNORE INTO {table_name} ({fields}) VALUES ({values})"
        return query
    
    def select(self, table_name, fields, condition=None):
        query = self.generate_select_query(table_name, fields, condition)
        self.connect()
        self.execute_request(query)
        all_rows = self.get_all_rows()
        self.close()
        return all_rows

    def generate_select_query(self, table_name, fields, condition):
        if condition:
            query = f'SELECT {fields} FROM {table_name} where {condition}'
        else:
            query = f'SELECT {fields} FROM {table_name}'
        return query

    def get_all_rows(self):
        return self.cursor.fetchall()
    
    def delete_rows(self, table_name, condition):
        query = self.delete_records_query(table_name, condition)
        self.run_database_query(query)
    
    def delete_records_query(self, table_name, condition):
        return f'DELETE FROM {table_name} WHERE {condition}'
    
    def get_max_id(self, table_name):
        query = f"SELECT MAX(id) FROM {table_name}"
        self.connect()
        self.execute_request(query)
        max_id = self.get_first_value()
        return max_id

    def get_first_value(self):
        row = self.cursor.fetchone()
        return row[MAX_VALUE_INDEX]
    
    def update_table(self, table_name, updates, condition=None):
        query = self.get_query_to_update_table(table_name, updates, condition)
        self.run_database_query(query)
    
    def get_query_to_update_table(self, table_name, updates, condition=None):
        if condition:
            query = f"UPDATE {table_name} SET {updates} where {condition}"
        else:
            query = f"UPDATE {table_name} SET {updates}"
        return query
