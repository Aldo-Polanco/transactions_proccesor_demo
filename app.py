import csv
import imp
import os
from functools import wraps
import jwt
import bcrypt
import json
from datetime import datetime
from datetime import timedelta
from utils.csv_proccesor import CsvProccesor
from utils.email_sender import EmailSender
from utils.misc import get_ls_at_path
from utils.misc import authenticate_user
from utils.misc import create_response
from utils.misc import get_input_create
from utils.misc import create_user_folder
from utils.dao import DataAccessObject
from utils.file_saver_manager import FileSaveManager
from config.database_config import db_config
from config.generic_config import generic_config
from flask import Flask
from flask import render_template
from flask import request
from flask import abort
import json

app = Flask(__name__)
dao = DataAccessObject(db_config['db_username'], db_config['db_password'],db_config["db_host"],db_config['db_name'])
secret_key = generic_config['app_secret']

def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', ' ').split()
        invalid_msg = {
            'message': 'Invalid token. Registeration and / or authentication required',
            'authenticated': False
        }
        expired_msg = {
            'message': 'Expired token. Reauthentication required.',
            'authenticated': False
        }
        if len(auth_headers) != 2:
            abort(401, invalid_msg)

        try:
            token = auth_headers[1]
            data = jwt.decode(token, secret_key, algorithms=['HS256'])
            user = dao.get_user_by_email(data['sub'])
            if not user:
                abort(422, 'User not found.')
            return f(user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            abort(401, expired_msg) # 401 is Unauthorized HTTP status code
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            abort(401, {
                'message': 'Unknow Error',
                'authenticated': False
            })
        except:
            abort(401, 'Error')

    return _verify

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/files/<file_name>', methods=["POST"])
@token_required
def proccess_user_file(logged_user, file_name):
    user_file_path = os.path.join('./user_files', str(logged_user['uid']), file_name)
    csv_proccesor = CsvProccesor(user_file_path)
    csv_proccesor.proccess_csv()
    html_template = render_template('transaction_email.html', user_name = logged_user['user_name'] ,**csv_proccesor.transaction_info)
    csv_proccesor.save_transactions_to_db(dao, logged_user['uid'], file_name)
    try:
        email_sender = EmailSender(generic_config['sender_email'],logged_user['user_email'],generic_config['smtp_server'],'Stori Card Transactions Resume!')
        email_sender.create_email_content(html_template)
        email_sender.send_email()
    except Exception as e:
        print(e)
    return html_template

@app.route('/user/files/api', methods =['GET'])
@token_required
def get_user_files_api(logged_user):
    user_folder_path = os.path.join('./user_files', str(logged_user['uid']))
    files = get_ls_at_path(user_folder_path)
    return create_response(json.dumps({"files":files}))

@app.route('/user/files', methods =['GET'])
def get_user_files():
    return render_template('user_files_list.html')

@app.route('/login/', methods=['GET', 'POST'])
def cli_login():
    if request.method == 'POST':
        try:
            data = request.get_json()
            user = authenticate_user(dao, **data)
            if not user:
                return create_response('{"error": "user not found"}', 401)

            token = jwt.encode({
                'sub': user['user_email'],
                'iat': datetime.utcnow(),
                'exp': datetime.utcnow() + timedelta(minutes=30)},
                secret_key)
            return create_response(json.dumps({ 'token': token }))
        except Exception as e:
            print(e)
            abort(401, 'Error')
    else:
        return render_template('login.html')

@app.route('/register/', methods=['GET'])
def cli_register():
    return render_template('register.html')

@app.route('/upload_file', methods = ['POST'])
@token_required
def upload_file(logged_user):
    user_folder_path = os.path.join('./user_files', str(logged_user['uid']))
    file_saver = FileSaveManager()
    file_saver.upload_file_to_folder(user_folder_path)
    return create_response(json.dumps({"status": 200, "new_file_name": file_saver.new_file_name}))

@app.route('/users', methods=['POST'])
def create_user():
    '''
       Create an user for the system.
    '''
    user_data = get_input_create(dao)
    for key in user_data.keys():
        if key == 'user_password':
            user_data[key] = bcrypt.hashpw(user_data[key].encode('utf8'), bcrypt.gensalt()).decode('utf8')
    user_data['uid'] = dao.save_user(user_data)
    create_user_folder(os.path.join('./user_files', str(user_data['uid'])))
    user_data.pop('user_password')
    return create_response(json.dumps(user_data))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)