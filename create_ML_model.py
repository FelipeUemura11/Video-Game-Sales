import os
import joblib
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Carregamento e pré-processamento dos dados
df = pd.read_csv('datasets/vgsales.csv')
df = df.dropna()

X = df[['Name', 'Platform', 'Year', 'Genre', 'Publisher']].copy()
y = df['Global_Sales']  # Alteração para prever apenas Global_Sales

label_encoders = {}
for column in ['Platform', 'Genre', 'Publisher']:
    le = LabelEncoder()
    X[column] = le.fit_transform(X[column])
    label_encoders[column] = le

scaler = StandardScaler()
X['Year'] = scaler.fit_transform(X[['Year']])

X_train, X_test, y_train, y_test = train_test_split(
    X.drop(columns=['Name']), y, test_size=0.2, random_state=42)

# Definição do modelo base
model = GradientBoostingRegressor(random_state=42)

# Definição do grid de parâmetros para o GridSearchCV
param_grid = {
    'n_estimators': [100, 200, 500],
    'learning_rate': [0.001, 0.01, 0.1],
    'max_depth': [3, 5, 7],
    'subsample': [0.5, 0.7, 1.0],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
}

# Configuração do GridSearchCV
grid_search = GridSearchCV(
    estimator=model,
    param_grid=param_grid,
    cv=5,
    scoring='neg_mean_squared_error',
    verbose=2,
    n_jobs=-1
)

# Execução do GridSearchCV para encontrar os melhores parâmetros
grid_search.fit(X_train, y_train)

# Extração do melhor modelo encontrado
best_model = grid_search.best_estimator_

# Avaliação do modelo no conjunto de teste
y_pred = best_model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)

print(f"Melhores Parâmetros: {grid_search.best_params_}")
print(f"MSE no Teste: {mse}")
print(f"MAE no Teste: {mae}")

# Salvamento do melhor modelo encontrado
if not os.path.exists('models/'):
    os.makedirs('models/')

joblib.dump({
    'model': best_model,
    'label_encoders': label_encoders,
    'scaler': scaler
}, 'models/best_model.pkl')

print("Melhor modelo salvo com sucesso em 'models/best_model.pkl'")