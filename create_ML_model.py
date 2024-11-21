import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from xgboost import XGBRegressor
from sklearn.multioutput import MultiOutputRegressor
import numpy as np
import matplotlib.pyplot as plt
import joblib

df = pd.read_csv('datasets/vgsales_clean.csv')

# Transformar as variáveis categóricas em variáveis numéricas e mapeando os valores originais
df['Publisher'] = df['Publisher'].astype('category')
publisher_categories = df['Publisher'].cat.categories
publisher_mapping = {publisher: code for code, publisher in enumerate(publisher_categories)}
publisher_inv_mapping = {code: publisher for publisher, code in publisher_mapping.items()}

df['Platform'] = df['Platform'].astype('category')
platform_categories = df['Platform'].cat.categories
platform_mapping = {platform: code for code, platform in enumerate(platform_categories)}
platform_inv_mapping = {code: platform for platform, code in platform_mapping.items()}

df['Genre'] = df['Genre'].astype('category')
genre_categories = df['Genre'].cat.categories
genre_mapping = {genre: code for code, genre in enumerate(genre_categories)}
genre_inv_mapping = {code: genre for genre, code in genre_mapping.items()}

# Substituir os valores de 'Publisher' pelos códigos numéricos
df['Publisher'] = df['Publisher'].cat.codes

# Criar a interação Platform_Genre
df['Platform_Genre'] = df['Platform'].cat.codes * df['Genre'].cat.codes

# Selecionar as features e os alvos
X = df[['Publisher', 'Platform_Genre', 'Year']].copy()
y = df[['Global_Sales', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']]

# Dividir os dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinar o modelo
xgb = XGBRegressor(random_state=42, max_depth=5, n_estimators=100, objective='reg:squarederror')
multi_output_xgb = MultiOutputRegressor(xgb)
multi_output_xgb.fit(X_train, y_train)

# Avaliar o modelo
y_pred = multi_output_xgb.predict(X_test)

sales_columns = ['Global_Sales', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']

for i, col in enumerate(sales_columns):
    mse = mean_squared_error(y_test[col], y_pred[:, i])
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test[col], y_pred[:, i])
    r2 = r2_score(y_test[col], y_pred[:, i])
    print(f"\nMétricas para {col}:")
    print(f"MSE: {mse:.4f}, RMSE: {rmse:.4f}, MAE: {mae:.4f}, R²: {r2:.4f}")

# Importância das features
feature_importances = np.zeros(len(X.columns))
for estimator in multi_output_xgb.estimators_:
    feature_importances += estimator.feature_importances_

# Média das importâncias
feature_importances /= len(multi_output_xgb.estimators_)

features = X.columns
indices = np.argsort(feature_importances)[::-1]

plt.figure(figsize=(8,6))
plt.title("Importância das Features - Média das Importâncias dos Modelos")
plt.bar(range(X.shape[1]), feature_importances[indices], align='center')
plt.xticks(range(X.shape[1]), [features[i] for i in indices])
plt.xlabel("Features")
plt.ylabel("Importância")
plt.show()
# As melhores features em ordem crescente são: Platform_Genre, Year, Publisher

import os

if not os.path.exists('models/'):
    os.makedirs('models/')

# Salvar o modelo treinado e os mapeamentos
joblib.dump({
    'model': multi_output_xgb,
    'publisher_mapping': publisher_mapping,
    'platform_mapping': platform_mapping,
    'genre_mapping': genre_mapping
}, 'models/best_model2.pkl')

print("\nModelo e mapeamentos salvos com sucesso!")