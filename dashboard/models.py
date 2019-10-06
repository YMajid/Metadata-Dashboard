import mysql.connector
from . import dashboard_db


class Tables(dashboard_db.Model):
    id = dashboard_db.Column(dashboard_db.Integer, primary_key=True)
    source = dashboard_db.Column(dashboard_db.String(120), nullable=False)
    table = dashboard_db.Column(dashboard_db.String(120), unique=True, nullable=False)
    description = dashboard_db.Column(dashboard_db.String(max), unique=True, nullable=False)

    def __repr__(self):
        return f"Tables('{self.source}', '{self.table}', '{self.description}')"


class Database():
    def __init__(self, host, user, password):
        self.db = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )

    def database_information(self):
        information = {}
        cursor = self.db.cursor()
        query1 = 'show databases;'
        cursor.execute(query1)
        databases = []
        for i in cursor.fetchall():
            databases.append(i[0])
        cursor.close()
        for database in databases:
            cursor = self.db.cursor()
            query2 = 'use {};'
            query3 = 'show full tables where Table_Type != "VIEW";'
            cursor.execute(query2.format(database))
            cursor.execute(query3)
            tables = []
            for j in cursor.fetchall():
                tables.append(j[0])
            cursor.close()
            table_information = {}
            for table in tables:
                cursor = self.db.cursor()
                query4 = 'show full columns from {}.{};'
                cursor.execute(query4.format(database, table))
                columns = cursor.fetchall()
                cursor.close()
                column_information = []
                for column in columns:
                    column_information.append({'Column':column[0], 'Type':column[1].split()[0], 'Comment':column[8]})
                table_information[table] = column_information
            information[database] = table_information
        return information

    def to_dashboard_db(self):
        information = self.database_information()
        # dashboard_db.session.query().delete()
        for i in information:
            for j in information[i]:
                table = Tables(source=i, table=j, description=information[i][j])
                dashboard_db.session.add(table)
        dashboard_db.session.commit()

