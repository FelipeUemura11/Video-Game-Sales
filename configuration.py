from flask import Flask

app = Flask(__name__)

# Configura a pasta de arquivos que foram enviados
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Verifica se o arquivo está na lista de tipos de arquivos aceitos
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS