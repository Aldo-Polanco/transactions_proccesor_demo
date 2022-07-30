import os
import bcrypt
from flask import make_response
from flask import request
from flask import abort

def get_ls_at_path(directory):
    files = os.listdir(directory)
    files.sort()
    dir_names = [name.split('/')[-1] for name in files if name.split('/')[-1] != 'proccesed']
    return dir_names

def authenticate_user(dao, **kwargs):
        email = kwargs.get('user_email')
        password = kwargs.get('user_password')
        if not email or not password:
            return None
        user = dao.get_user_by_email(email)
        if user:
            stored_hash = user['user_password'].encode('utf-8')
            if not bcrypt.checkpw(password.encode('utf-8'), \
                                             stored_hash):
                return None

        return user

def create_response(json_string, content_type = 'application/json', status_code = 200):
    response = make_response(json_string)                                           
    response.headers['Content-Type'] = '{0}; charset=utf-8'.format(content_type)
    response.status_code = status_code            
    return response

def get_input_create(dao):
    '''
        Metodo para validar el input para crear usuario.
    '''
    data = {}
    if 'user_name' in request.json:
        data['user_name'] = request.json['user_name']
    else:
        abort(422, 'Need "user_name" on input.')
    if('user_email' in request.json):
        user = dao.get_user_by_email(request.json['user_email'])
        if not user:
            data['user_email'] = request.json['user_email']
        else:
            abort(422, '"user_email" already in use.')
    else:
        abort(422, '"user_email" not in input".')
    if 'user_password' not in request.json:
        abort(422, '"user_password" not in input.')
    else:
        data['user_password'] = request.json['user_password']
    return data

def create_user_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)