# ═══════════════ஜ۩۞۩ஜ═══════════════

# Video Game Sales

## Data Set
- **Nome**: Video Game Sales
- **Descrição**: Este conjunto de dados contém uma lista de jogos de vídeo com vendas superiores a 100.000 cópias. 
- Ele foi gerado por um usuário do Kaggle e contém informações sobre vendas globais e por região, além de informações 
- sobre o gênero, a plataforma e a editora de cada jogo.
- **Fonte**: [Video Game Sales](https://www.kaggle.com/gregorut/videogamesales)

## Integrantes

   - Dayane Dias Negrello
   - Enzo Heiden Januario
   - Felipe Yukiya Soares Uemura
   - John Claude Cameron Chappell

# ═══════════════ஜ۩۞۩ஜ═══════════════

# Instalação

---
1. Clone o [repositório](https://github.com/FelipeUemura11/Video-Game-Sales).
2. Abra o PyCharm e adicione o ambiente virtual (venv).
3. Abra o arquivo "_app.py_".
4. Clique em "_Create a virtual environment using requirements.txt_" no canto superior direito.
![Create With requirements.png](ReadME%20Files%2FCreate%20With%20requirements.png)
5. Caso não apareça a opção para criar o ambiente virtual usando o "_requirements.txt_", adicione o ambiente virtual e aguarde até aparecer um aviso para instalar os pacotes necessários.
6. Clique em "_Install Requirements_" e aguarde até que todos os pacotes sejam instalados.
![Install requirements.png](ReadME%20Files%2FInstall%20requirements.png)
7. Após a instalação, execute o arquivo "_app.py_".
8. Abra o link que aparece no console "_http://127.0.0.1:5000_" (verifique a porta).

Se preferir aqui está a lista de todos os pip install necessários:
```
pip install Flask~=3.1.0
pip install pandas~=2.2.3
pip install joblib~=1.4.2
pip install matplotlib~=3.9.2
pip install plotly~=5.24.1
pip install scikit-learn~=1.5.2
pip install numpy~=2.1.3
pip install xgboost~=2.1.2
pip install seaborn~=0.13.2
```

# Estrutura do Projeto

## app.py
- **Páginas da Web**:
1. Página inicial que limpa o arquivo anterior carregado e define o tema.
2. Dashboard: Página do dashboard.
3. Upload: Permite o upload de arquivos .csv e os salva na pasta especificada.
4. Predict: Recebe informações do utilizador para prever as vendas de jogos, utilizando funções de data.py.
5. Analytics: Carrega a página de análise.
6. Get-visualizations: gera visualizações de dados usando vizualizations.py e as retorna como JSON.
7. Interactive_plot: gera um gráfico interativo e o renderiza.

- **Relacionamento**:
  - Utiliza funções de data.py para carregar dados e realizar predições, e vizualizations.py para gerar visualizações.

## data.py
- **Funções**:
   - ler_dados(upload_folder): Lê o arquivo CSV carregado e o armazena em uma variável global.
   - predict_game(input_data): Realiza predições de vendas usando o modelo treinado e mapeamentos previamente salvos.

### Relacionamento com app.py:
- As funções são chamadas em app.py para carregar dados e fazer predições de jogos na página de previsão (/predict).

## vizualizations.py
- **Funções**:
   - Gera gráficos e visualizações usando matplotlib, seaborn e plotly.
   - generate_visualizations(df, theme): Cria várias visualizações, incluindo gráficos de vendas por plataforma e região.
   - gerar_plot_interativo(df, theme): Gera um gráfico interativo sobre vendas ao longo do tempo.

### Relacionamento com app.py:
- generate_visualizations é usada para criar gráficos e enviar visualizações ao usuário pela página /get-visualizations.
- gerar_plot_interativo é utilizada em /interactive_plot.

## configuration.py
- **Configuração**:
  - Cria o objeto Flask para o aplicativo ‘web’.
  - Define o UPLOAD_FOLDER como a pasta de ‘uploads’ e garante que exista.
  - Define a chave secreta para gerir sessões.

### Relacionamento com _app.py_:
- _app.py_ importa app de configuration.py para configurar o servidor Flask, incluindo diretórios e chaves.

## create_ML_model.py
- **Funções**:
  - Carrega os dados de um CSV (vgsales_clean.csv) e transforma variáveis categóricas em numéricas.
  - Treina um modelo XGBRegressor para prever vendas globais e regionais de jogos.
  - Avalia o modelo usando métricas como MSE, RMSE, MAE e R².
  - Salva o modelo treinado e mapeamentos (publicadora, plataforma, gênero) em models/best_model2.pkl.

### Relacionamento com app.py:
- O modelo salvo é carregado por data.py para realizar predições, que são usadas na página /predict de app.py.
