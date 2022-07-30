import sqlalchemy
import os

class DataAccessObject():

    def __init__(self, username, db_password, db_host, db_name):
        self.db = sqlalchemy.create_engine(
            sqlalchemy.engine.url.URL(
                drivername="postgresql+psycopg2",
                username= username,
                password= db_password,
                host= db_host,
                database= db_name,
            ),
            pool_size=5,
            max_overflow=2,
            pool_timeout=30,  # 30 seconds
            pool_recycle=1800,  # 30 minutes
        )

    def get_user_by_email(self, email):
        sql = f'''
            Select * from users where user_email = '{email}'
        '''
        return self.get_anything(sql,None)

    def save_user(self, user_data):
        sql = '''
            INSERT INTO users (user_name, user_email, user_password) VALUES (%s,%s,%s)
        '''
        values =(user_data['user_name'], user_data['user_email'], user_data['user_password'])
        self.save_anything(sql, values)
        return self.get_user_by_email(user_data['user_email'])['uid']

    def get_anything(self, sql, data = None, first_one = True):
        with self.db.connect() as conn:
            resultproxy = conn.execute(sql) if data is None else conn.execute(sql, data)
            row = [dict(rowproxy.items()) for rowproxy in resultproxy]
        if row and first_one:
            return row[0]
        if len(row):
            return row
        if not len(row) and not first_one:
            return []
        return None

    def save_anything(self, sql, data = None):
        with self.db.connect() as conn:
            result = conn.execute(sql, data) if data else conn.execute(sql)
        return result.lastrowid

    def save_transaction(self,user_id, transaction_info):
        sql = f"""
            INSERT INTO transactions (doc_id, doc_date, transaction_value, users_id, doc_source) 
            VALUES (
                {transaction_info['Id']},
                '{transaction_info['Date']}',
                {transaction_info['Transaction']},
                {user_id},
                '{transaction_info['doc_source']}'
            )
        """
        return self.save_anything(sql)