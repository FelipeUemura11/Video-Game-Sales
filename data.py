import pandas as pd
import joblib
import os

def ler_dados(upload_folder):
    global df_global
    files = os.listdir(upload_folder)

    if len(files) == 0:
        raise ValueError('Nenhum arquivo encontrado.')
    elif len(files) > 1:
        raise ValueError('Múltiplos arquivos encontrados. Por favor, mantenha apenas um arquivo na pasta "uploads".')
    else:
        file_path = os.path.join(upload_folder, files[0])

        if not file_path.endswith('.csv'):
            raise ValueError('Formato de arquivo inválido. Apenas arquivos .csv são suportados.')
        else:
            df_global = pd.read_csv(file_path)
            df_global = df_global.dropna()

            return df_global


def predict_game(input_data):
    try:
        print("Iniciando predição com os dados de entrada:", input_data)

        # Carregar o modelo e os mapeamentos
        loaded_data = joblib.load('models/best_model.pkl')
        model = loaded_data['model']
        publisher_mapping = loaded_data['publisher_mapping']
        platform_mapping = loaded_data['platform_mapping']
        genre_mapping = loaded_data['genre_mapping']
        print("Modelo e mapeamentos carregados com sucesso.")

        # Extrair os dados de entrada
        publisher = input_data.get('Publisher')
        platform = input_data.get('Platform')
        genre = input_data.get('Genre')
        year = input_data.get('Year')

        # Mapear os dados de entrada
        publisher_code = publisher_mapping.get(publisher)
        if publisher_code is None:
            publisher_code = -1
        platform_code = platform_mapping.get(platform)
        if platform_code is None:
            platform_code = -1

        genre_code = genre_mapping.get(genre)
        if genre_code is None:
            genre_code = -1

        # Criar a interação Platform_Genre
        platform_genre = platform_code * genre_code

        # Criar o DataFrame de entrada com as features necessárias
        input_features = {
            'Publisher': [publisher_code],
            'Platform_Genre': [platform_genre],
            'Year': [year]
        }

        input_df = pd.DataFrame(input_features)

        # Fazer a predição
        prediction = model.predict(input_df)

        # Retornar a predição como um dicionário
        sales_columns = ['Global_Sales', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']
        prediction_dict = dict(zip(sales_columns, prediction.flatten().tolist()))
        return {k: round(v, 2) for k, v in prediction_dict.items()}

    except Exception as e:
        return f"Erro na predição: {str(e)}"