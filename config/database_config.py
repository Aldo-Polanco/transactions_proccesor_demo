import os

db_config = {
    'db_username' : os.getenv('DB_USERNAME'),
    'db_password' : os.getenv('DB_PASSWORD'),
    'db_host' : os.getenv('DB_HOST'),
    'db_name' : os.getenv('DB_NAME')
}
