from utils.dao import DataAccessObject
from config.database_config import db_config

dao = DataAccessObject(db_config['db_username'], db_config['db_password'],db_config["db_host"],db_config['db_name'])

if __name__ == '__main__':
    try:
        dao.save_anything('''
                create table public.users (
                    uid serial NOT NULL PRIMARY key,
                    user_name varchar(45) not null,
                    user_email varchar(100) not null,
                    user_password text not null
                );

                create table public.transactions (
                    uid serial NOT NULL PRIMARY key,
                    users_id smallint not null,
                    doc_id INT not null,
                    doc_source varchar(100) null,
                    doc_date DATE NOT null,
                    transaction_value float not null,
                    CONSTRAINT fk_us
                    FOREIGN KEY(users_id) 
                    REFERENCES users(uid)
                );        
        ''')
    except Exception as e:
        print(e)       