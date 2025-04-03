import os

from flask import render_template, request, redirect, url_for, session, flash, jsonify

from configuration import app
from data import ler_dados, predict_game
from vizualizations import generate_visualizations, gerar_plot_interativo

def set_theme():
    theme = request.cookies.get('theme', 'light')
    session['theme'] = theme

@app.route('/', methods=['GET', 'POST'])
def index():
    set_theme()

    session.pop('uploaded_file', None)

    upload_folder = app.config['UPLOAD_FOLDER']
    for filename in os.listdir(upload_folder):
        file_path = os.path.join(upload_folder, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    return render_template('index.html', home_button=False)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    set_theme()
    uploaded_file = session.get('uploaded_file', None)
    return render_template('dashboard.html', home_button=True, uploaded_file=uploaded_file)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    set_theme()
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.csv'):
            previous_file = session.get('uploaded_file', None)
            if previous_file:
                old_filepath = os.path.join(app.config['UPLOAD_FOLDER'], previous_file)
                if os.path.exists(old_filepath):
                    os.remove(old_filepath)
                flash(f"O arquivo anterior ('{previous_file}') foi substituído.")

            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            try:
                file.save(filepath)
                session['uploaded_file'] = file.filename
                flash(f"O arquivo '{file.filename}' foi carregado com sucesso.")
                return redirect(url_for('dashboard'))
            except Exception as e:
                flash(f"Erro ao salvar o arquivo: {str(e)}")
                return redirect(url_for('upload'))
        elif not file:
            flash("Nenhum arquivo selecionado.")
            return redirect(url_for('upload'))
        else:
            flash("Formato de arquivo inválido. Apenas arquivos .csv são suportados.")
            return redirect(url_for('upload'))
    return render_template('upload.html', home_button=True)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    set_theme()
    df = ler_dados(app.config['UPLOAD_FOLDER'])

    publishers = df['Publisher'].unique()
    platforms = df['Platform'].unique()
    genres = df['Genre'].unique()

    result = None
    input_data = None

    if request.method == 'POST':
        input_data = {
            "Name": request.form.get('Name'),
            "Platform": request.form.get('Platform'),
            "Year": int(request.form.get('Year')),
            "Genre": request.form.get('Genre'),
            "Publisher": request.form.get('Publisher')
        }

        result = predict_game(input_data)
        print(input_data)

    return render_template(
        'predictions.html',
        home_button=True,
        platforms=platforms,
        genres=genres,
        publishers=publishers,
        game=input_data,
        result=result
    )

@app.route('/analytics', methods=['GET'])
def analytics():
    return render_template('analytics.html', home_button=True)

@app.route('/get-visualizations', methods=['GET'])
def get_visualizations():
    theme = request.cookies.get('theme', 'light')

    df = ler_dados(app.config['UPLOAD_FOLDER'])

    try:
        visualizations = generate_visualizations(df, theme)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    # Retorna os gráficos como JSON
    return jsonify({'visualizations': visualizations})


@app.route('/interactive_plot', methods=['GET', 'POST'])
def interactive_plot():
    set_theme()

    theme = request.cookies.get('theme', 'light')

    df = ler_dados(app.config['UPLOAD_FOLDER'])

    grafico_interativo = gerar_plot_interativo(df, theme)

    return render_template('interactive_plot.html', home_button=True, interactive_plot=grafico_interativo)

if __name__ == '__main__':
    print("Iniciando o servidor...")
    app.run(debug=True)

