import pandas as pd
import joblib
import os

df_global = None

def ler_dados(upload_folder):
    global df_global
    files = os.listdir(upload_folder)

    if len(files) == 0:
        return ValueError('Nenhum arquivo encontrado.')
    elif len(files) > 1:
        return ValueError('Múltiplos arquivos encontrados. Por favor, mantenha apenas um arquivo na pasta "uploads".')
    else:
        file_path = os.path.join('uploads/', files[0])

        if not file_path.endswith('.csv'):
            return ValueError('Formato de arquivo inválido. Apenas arquivos .csv são suportados.')
        else:
            df_global = pd.read_csv(file_path)
            df_global = df_global.dropna()
            return df_global


def predict_game(input_data):
    try:
        print("Iniciando predição com os dados de entrada:", input_data)

        # Carregar o modelo e os objetos de pré-processamento
        loaded_data = joblib.load('models/best_model.pkl')
        model = loaded_data['model']
        label_encoders = loaded_data['label_encoders']
        scaler = loaded_data['scaler']
        print("Modelo e pré-processadores carregados com sucesso.")

        # Criar um DataFrame a partir dos dados de entrada
        input_df = pd.DataFrame([input_data])
        print("DataFrame de entrada criado:", input_df)

        # Aplicar o mesmo pré-processamento que foi aplicado aos dados de treino
        for column in ['Platform', 'Genre', 'Publisher']:
            if column in input_df.columns:
                le = label_encoders[column]
                if input_df[column].iloc[0] in le.classes_:
                    input_df[column] = le.transform(input_df[column])
                else:
                    # Lidar com categorias não vistas anteriormente
                    input_df[column] = -1  # Ou outro valor padrão
                    print(f"Valor não visto na coluna '{column}':", input_df[column].iloc[0])
            else:
                error_message = f"Coluna '{column}' não encontrada nos dados de entrada."
                print(error_message)
                return error_message

        # Padronização da coluna 'Year'
        if 'Year' in input_df.columns:
            input_df['Year'] = scaler.transform(input_df[['Year']])
        else:
            error_message = "Coluna 'Year' não encontrada nos dados de entrada."
            print(error_message)
            return error_message

        # Selecionar as colunas na ordem correta
        features = ['Platform', 'Year', 'Genre', 'Publisher']
        input_df = input_df[features]
        print("Dados de entrada após pré-processamento:", input_df)

        # Fazer a predição
        prediction = model.predict(input_df)
        print("Predição realizada com sucesso:", prediction)

        # Retornar a predição como um dicionário
        sales_columns = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']
        prediction_dict = dict(zip(sales_columns, prediction.flatten().tolist()))
        print("Resultado da predição:", prediction_dict)
        return {k: round(v, 2) for k, v in prediction_dict.items()}
    except Exception as e:
        error_message = f"Erro na predição: {str(e)}"
        print(error_message)
        return error_message