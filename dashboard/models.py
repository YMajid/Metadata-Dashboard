import mysql.connector
from dashboard import dashboard_db


class Tables(dashboard_db.Model):
    id = dashboard_db.Column(dashboard_db.Integer, primary_key=True)
    source = dashboard_db.Column(dashboard_db.String(120), nullable=False)
    table = dashboard_db.Column(dashboard_db.String(120), unique=True, nullable=False)
    description = dashboard_db.Column(dashboard_db.String(max), unique=True, nullable=False)

    def __repr__(self):
        return f"User('{self.source}', '{self.table}', '{self.description}')"


class Database():
    def __init__(self, host, user, password):
        self.db = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )

    def show_databases(self):
        cursor = self.db.cursor()
        query = 'show databases;'
        databases_names = []
        cursor.execute(query)
        for i in cursor.fetchall():
            databases_names.append(i[0])
        cursor.close()
        return databases_names

    def show_tables(self):
        cursor = self.db.cursor()
        databases = self.show_databases()
        query_database = 'use {};'
        query_tables = 'show full tables where Table_Type != "VIEW";'
        tables_names = []
        for database in databases:
            cursor.execute(query_database.format(database))
            cursor.execute(query_tables)
            tables = cursor.fetchall()
            if len(tables) > 0:
                for table in tables:
                    tables_names.append('{}.{}'.format(database, table[0]))
        cursor.close()
        return tables_names

    def describe_tables(self):
        cursor = self.db.cursor()
        tables = self.show_tables()
        table_descriptions = {}
        column_descriptions = {}
        query = 'show full columns from {}'
        for table in tables:
            cursor.execute(query.format(table))
            for column in cursor:
                column_descriptions[column[0]] = {'Type':column[1].split()[0], 'Key':column[4], 'Comment':column[8]}
            table_descriptions[table] = column_descriptions
        cursor.close()
        return table_descriptions
