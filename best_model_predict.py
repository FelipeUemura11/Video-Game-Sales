# Importar as bibliotecas necessárias
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Carregar o conjunto de dados
dados = pd.read_csv('datasets/vgsales.csv')

# Selecionar as características e o alvo
caracteristicas = ['Platform', 'Year', 'Genre', 'Publisher']
alvo = 'Global_Sales'

X = dados[caracteristicas]
y = dados[alvo]

# Tratar valores faltantes
X = X.dropna()
y = y[X.index]

# Não aplicar transformação logarítmica na variável alvo
# y_log = np.log1p(y)

# Agrupar publishers raros
publisher_counts = X['Publisher'].value_counts()
rare_publishers = publisher_counts[publisher_counts < 50].index
X['Publisher'] = X['Publisher'].replace(rare_publishers, 'Other')

# Criar novas características
platform_sales = dados.groupby('Platform')['Global_Sales'].mean()
X['Platform_Mean_Sales'] = X['Platform'].map(platform_sales)

genre_sales = dados.groupby('Genre')['Global_Sales'].mean()
X['Genre_Mean_Sales'] = X['Genre'].map(genre_sales)

# Atualizar a lista de características
categorical_features = ['Platform', 'Genre', 'Publisher']
numeric_features = ['Year', 'Platform_Mean_Sales', 'Genre_Mean_Sales']

# Tratar valores faltantes nas novas características
X['Platform_Mean_Sales'] = X['Platform_Mean_Sales'].fillna(platform_sales.mean())
X['Genre_Mean_Sales'] = X['Genre_Mean_Sales'].fillna(genre_sales.mean())

# Dividir em conjuntos de treinamento e teste
X_treino, X_teste, y_treino, y_teste = train_test_split(
    X, y, test_size=0.2, random_state=42)

# Atualizar publishers nos conjuntos de teste
X_teste['Publisher'] = X_teste['Publisher'].replace(rare_publishers, 'Other')

# Definir o pré-processador
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
        ('num', StandardScaler(), numeric_features)
    ])

# Criar o pipeline que combina o pré-processador e o modelo
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', XGBRegressor(
        n_estimators=1000,
        learning_rate=0.01,
        max_depth=6,
        random_state=42,
        verbosity=0
    ))
])

# Ajustar o pipeline nos dados de treinamento
pipeline.fit(X_treino, y_treino)

# Fazer previsões no conjunto de teste
y_pred = pipeline.predict(X_teste)

# Calcular o erro quadrático médio
mse = mean_squared_error(y_teste, y_pred)
print(f'Erro Quadrático Médio: {mse:.4f}')

# Calcular o RMSE
rmse = np.sqrt(mse)
print(f'RMSE: {rmse:.4f} milhões de unidades')

# Calcular o R²
r2 = r2_score(y_teste, y_pred)
print(f'R²: {r2:.4f}')

# Exemplo de previsão com um novo jogo
# Detalhes do jogo hipotético
jogo_novo = pd.DataFrame({
    'Platform': ['X360'],
    'Year': [2016],
    'Genre': ['Action'],
    'Publisher': ['Microsoft Game Studios']
})

# Tratar publishers raros no novo jogo
jogo_novo['Publisher'] = jogo_novo['Publisher'].replace(rare_publishers, 'Other')

# Criar novas características para o novo jogo
jogo_novo['Platform_Mean_Sales'] = jogo_novo['Platform'].map(platform_sales)
jogo_novo['Genre_Mean_Sales'] = jogo_novo['Genre'].map(genre_sales)

# Tratar valores faltantes nas novas características
jogo_novo['Platform_Mean_Sales'] = jogo_novo['Platform_Mean_Sales'].fillna(platform_sales.mean())
jogo_novo['Genre_Mean_Sales'] = jogo_novo['Genre_Mean_Sales'].fillna(genre_sales.mean())

# Fazer a previsão
venda_prevista = pipeline.predict(jogo_novo)
print(f'Vendas Globais Previstas: {venda_prevista[0]:.2f} milhões de unidades')
