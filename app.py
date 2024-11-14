from flask import render_template, request, redirect, url_for, flash
from configuration import app, allowed_file
from werkzeug.utils import secure_filename
import os

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Nenhum arquivo encontrado na requisição')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('Nenhum arquivo selecionado para upload')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            flash('Arquivo enviado com sucesso!')
            return redirect(url_for('upload'))
        else:
            flash('Tipos de arquivo permitidos: txt, pdf, png, jpg, jpeg, gif')
            return redirect(request.url)

    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
