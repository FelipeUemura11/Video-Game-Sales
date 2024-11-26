# ═══════════════ஜ۩۞۩ஜ═══════════════
 - Vide Games Sales
 - Data Set: https://www.kaggle.com/datasets/gregorut/videogamesales
 - ======= Integrantes =======
   - Felipe Yukiya Soares Uemura 
   - John Claude Cameron Chappell 
   - Enzo Heiden Januario 
   -  Dayane Dias Negrello 
# ═══════════════ஜ۩۞۩ஜ═══════════════

1. app.py
Páginas da Web:
Página inicial que limpa o arquivo anterior carregado e define o tema.
dashboard: Página do dashboard.
upload: Permite o upload de arquivos .csv e os salva na pasta especificada.
predict: Recebe informações do usuário para prever as vendas de jogos, utilizando funções de data.py.
analytics: Carrega a página de análise.
get-visualizations: Gera visualizações de dados usando vizualizations.py e as retorna como JSON.
interactive_plot: Gera um gráfico interativo e o renderiza.
Relacionamento:
Utiliza funções de data.py para carregar dados e realizar predições, e vizualizations.py para gerar visualizações.
2. data.py
Funções:
ler_dados(upload_folder): Lê o arquivo CSV carregado e o armazena em uma variável global.
predict_game(input_data): Realiza predições de vendas usando o modelo treinado e mapeamentos previamente salvos.
Relacionamento com app.py:
As funções são chamadas em app.py para carregar dados e fazer predições de jogos na página de previsão (/predict).
3. vizualizations.py
Funções:
Gera gráficos e visualizações usando matplotlib, seaborn e plotly.
generate_visualizations(df, theme): Cria várias visualizações, incluindo gráficos de vendas por plataforma e região.
gerar_plot_interativo(df, theme): Gera um gráfico interativo sobre vendas ao longo do tempo.
Relacionamento com app.py:
generate_visualizations é usada para criar gráficos e enviar visualizações ao usuário pela página /get-visualizations.
gerar_plot_interativo é utilizada em /interactive_plot.
4. configuration.py
Configuração:
Cria o objeto Flask para o aplicativo web.
Define o UPLOAD_FOLDER como a pasta de uploads e garante que exista.
Define a chave secreta para gerenciar sessões.
Relacionamento com app.py:
app.py importa app de configuration.py para configurar o servidor Flask, incluindo diretórios e chaves.
5. create_ML_model.py
Funções:
Carrega os dados de um CSV (vgsales_clean.csv) e transforma variáveis categóricas em numéricas.
Treina um modelo XGBRegressor para prever vendas globais e regionais de jogos.
Avalia o modelo usando métricas como MSE, RMSE, MAE e R².
Salva o modelo treinado e mapeamentos (publicadora, plataforma, gênero) em models/best_model2.pkl.
Relacionamento com app.py:
O modelo salvo é carregado por data.py para realizar predições, que são usadas na página /predict de app.py.
