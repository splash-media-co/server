from logs import Info, Warning, Debug, Error, Critical  # noqa: F401
import sqlite3  # noqa: F401


class OceanDB:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(f"{db_name}.sqlite")
        self.cursor = self.conn.cursor()
        Info(f"Connected to {db_name}.sqlite!")

    def commit(self):
        self.conn.commit()

    def insert_data(self, table_name, values):
        placeholders = ",".join(["?" for _ in values])
        sql = f"INSERT INTO {table_name} VALUES ({placeholders})"
        self.cursor.execute(sql, values)
        self.commit()

    def select_data(self, table_name, conditions=None):
        query = f"SELECT * FROM {table_name}"

        if conditions:
            conditions_str = " AND ".join([f"{key} = ?" for key in conditions])
            query += f" WHERE {conditions_str}"

        self.cursor.execute(query, tuple(conditions.values()) if conditions else ())
        return self.cursor.fetchall()

    def update_data(self, table_name, update_data, conditions=None):
        query = f"UPDATE {table_name} SET "

        # Construct the SET part of the query with the update_data dictionary
        set_values = ", ".join([f"{key} = ?" for key in update_data])
        query += set_values

        # Add a WHERE clause if conditions are provided
        if conditions:
            conditions_str = " AND ".join([f"{key} = ?" for key in conditions])
            query += f" WHERE {conditions_str}"

        # Execute the update query
        self.cursor.execute(query, tuple(update_data.values()) + tuple(conditions.values()) if conditions else tuple(update_data.values()))
        self.commit()

    def delete_data(self, table_name, conditions=None):
        query = f"DELETE FROM {table_name}"

        # Add a WHERE clause if conditions are provided
        if conditions:
            conditions_str = " AND ".join([f"{key} = ?" for key in conditions])
            query += f" WHERE {conditions_str}"

        # Execute the delete query
        self.cursor.execute(query, tuple(conditions.values()) if conditions else ())
        self.commit()
        Warning(f"Deleted data from {table_name}")

    def close(self):
        self.conn.close()
        Info(f"Closed database {self.db_name}")