import os

generic_config = {
    'files_root_path' : os.getenv('FILE_ROOT_PATH','./user_files'),
    'sender_email' : os.getenv('SENDER_EMAIL'),
    'sender_email_password' : os.getenv('SENDER_EMAIL_PASS'),
    'db_name' : os.getenv('DB_NAME'),
    'app_secret': os.getenv('APP_SECRET'),
    'smtp_server': os.getenv('SMTP_SERVER')
}
