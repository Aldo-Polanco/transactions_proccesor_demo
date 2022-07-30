from flask import request
from flask import abort
import uuid
import os

class FileSaveManager():

    def get_request_file(self):
        '''
            Encargada de darte el file que mando el front end
            y validar
        '''
        if 'file' not in request.files:
            abort(400, 'Peticion sin archivo.')
        return request.files['file']

    def upload_file_to_folder(self, file_path):
        '''
            Encargado de subir el documento a un proyecto
        '''
        file = self.get_request_file()
        file_uudi = uuid.uuid4().urn[9:13]
        if not self.file_extension_validation(file.filename):
            abort(400, 'Solo .csv')
        self.new_file_name = f'{file.filename.rsplit(".", 1)[0].lower()}_{file_uudi}.csv'
        path_to_save = os.path.join(file_path, self.new_file_name)
        file.save(path_to_save)
        return True

    def file_extension_validation(self, filename):
        '''
            Valida que la extensión del archivo a subir y
            setea la variable para la extensión del archivo
            para usarse mas adelante.

            Args:
                filename (str): Nombre del archivo a subir.

            Returns:
                Bool: True si es valido, False si no tiene la extensión correcta
        '''
        self.file_extension = filename.rsplit('.', 1)[1].lower()
        return '.' in filename and self.file_extension in ['txt', 'csv', 'xls', 'xlsx']