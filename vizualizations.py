import base64
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from io import BytesIO


def generate_visualizations(df, theme):
    sns.set_theme(style='darkgrid' if theme == 'dark' else 'whitegrid')

    visualizations = [{
        'imagem': gerar_imagem(sales_per_plataform, df, theme)
    }, {
        'imagem': gerar_imagem(regional_sales, df, theme)
    }, {
        'imagem': gerar_imagem(sales_per_genre_NA, df, theme)
    }, {
        'imagem': gerar_imagem(sales_per_genre_EU, df, theme)
    }, {
        'imagem': gerar_imagem(sales_per_genre_JP, df, theme)
    }, {
        'imagem': gerar_imagem(hist_sales_per_platform, df, theme)
    }, {
        'imagem': gerar_imagem(hist_sales_per_year, df, theme)
    }, {
        'imagem': gerar_imagem(sales_per_publisher_NA, df, theme)
    }, {
        'imagem': gerar_imagem(sales_per_publisher_EU, df, theme)
    }, {
        'imagem': gerar_imagem(sales_per_publisher_JP, df, theme)
    }, {
        'imagem': gerar_imagem(genero_predominante_regiao, df, theme)
    }]

    return visualizations


def gerar_imagem(plot_function, df, theme):
    buffer = BytesIO()

    background_color = (43 / 255, 48 / 255, 53 / 255, 0.0) if theme == 'dark' else (1, 1, 1, 0.0)

    fig, ax = plt.subplots(figsize=(12, 6), facecolor=background_color)
    ax.set_facecolor(background_color)

    plot_function(df, ax, theme)

    plt.savefig(buffer, format='png', bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close(fig)

    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()

    return f"data:image/png;base64,{img_base64}"


def gerar_plot_interativo(df, theme):
    sales_over_time = df.groupby('Year')['Global_Sales'].sum().reset_index()

    line_color = 'blue' if theme == 'light' else '#FFFF12'

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=sales_over_time['Year'],
        y=sales_over_time['Global_Sales'],
        mode='lines+markers',
        marker=dict(size=6, color=line_color),  # Cor dos marcadores
        line=dict(width=2, color=line_color, dash='solid')  # Propriedades da linha
    ))

    # Definir cores com base no tema
    background_color = '#2B3035' if theme == 'dark' else '#FFFFFF'
    text_color = '#FFFFFF' if theme == 'dark' else '#000000'
    grid_color = 'lightgrey' if theme == 'light' else '#444444'
    zero_line_color = text_color

    fig.update_layout(
        title='Vendas Globais ao Longo do Tempo',
        xaxis_title='Ano',
        yaxis_title='Vendas Globais (em milhões)',
        hovermode='x unified',
        font=dict(size=12, weight='bold', color=text_color),
        xaxis=dict(
            showgrid=False,
            color=text_color,
            tickfont=dict(color=text_color),
            titlefont=dict(color=text_color)
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=grid_color,
            color=text_color,
            tickfont=dict(color=text_color),
            titlefont=dict(color=text_color),
            zeroline=True,
            zerolinecolor=zero_line_color
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        width=1600,
        height=530
    )

    return fig.to_html(full_html=False, include_plotlyjs='cdn')


def sales_per_plataform(df, ax, theme):
    sales_per_platform = df.groupby('Platform')['Global_Sales'].sum() / 1000
    sales_per_platform = sales_per_platform.reset_index()
    order = sales_per_platform.sort_values(by='Global_Sales', ascending=False)['Platform']

    text_color = "#FFFFFF" if theme == 'dark' else "#000000"

    sns.barplot(x='Platform', y='Global_Sales', data=sales_per_platform, order=order, color='#dc6fed', ax=ax)

    ax.set_title('Total de Vendas por Plataforma', fontweight='bold', color=text_color)
    ax.set_ylabel('Total de Vendas (em bilhão)', color=text_color)
    ax.set_xlabel('Plataforma', color=text_color)
    ax.tick_params(axis='x', colors=text_color, rotation=90)
    ax.tick_params(axis='y', colors=text_color)

    ax.grid(True, linestyle='--', alpha=0.7, color='#FFFFFF')


def regional_sales(df, ax, theme):
    regional_sales = df[['NA_Sales', 'EU_Sales', 'JP_Sales']].sum() / 1000

    text_color = "#FFFFFF" if theme == 'dark' else "#000000"

    regional_sales.plot(kind='barh', color=['#9af252', '#edf252', '#e6844c'], ax=ax)

    ax.set_title('Vendas Totais de Jogos por Região', fontweight='bold', color=text_color)
    ax.set_xlabel('Total de Vendas (bilhões)', color=text_color)
    ax.set_ylabel('Região', rotation=0, color=text_color)
    ax.tick_params(axis='x', colors=text_color)
    ax.tick_params(axis='y', colors=text_color, rotation=45)

    ax.grid(True, linestyle='--', alpha=0.7, color='#FFFFFF')


def genero_predominante_regiao(df, ax, theme):
    valores_por_regiao = df.groupby('Genre')[['NA_Sales', 'EU_Sales', 'JP_Sales']].sum()
    valores_por_regiao = valores_por_regiao.reset_index()

    # Normaliza as vendas para comparação proporcional
    valores_por_regiao_normalizado = valores_por_regiao.set_index('Genre').apply(lambda x: x / x.sum(), axis=0)

    text_color = "#FFFFFF" if theme == 'dark' else "#000000"
    colors = sns.color_palette("Set2", len(valores_por_regiao_normalizado))

    valores_por_regiao_normalizado.plot(
        kind='bar',
        stacked=False,
        figsize=(10, 6),
        color=colors,
        ax=ax
    )

    ax.set_title('Gêneros Mais Predominantes por Região', fontweight='bold', color=text_color)
    ax.set_xlabel('Gênero', color=text_color)
    ax.set_ylabel('Proporção de Vendas', color=text_color)
    ax.tick_params(axis='x', rotation=45, colors=text_color)
    ax.tick_params(axis='y', colors=text_color)
    ax.legend(title='Região', loc='upper left', fontsize=10, title_fontsize=12, facecolor='white')

    ax.grid(True, linestyle='--', alpha=0.7, color='#FFFFFF')


def sales_per_genre_NA(df, ax, theme):
    sales_by_genre = df.groupby('Genre')['NA_Sales'].sum().reset_index()
    sales_by_genre = sales_by_genre.sort_values(by='NA_Sales', ascending=False)

    colors = sns.color_palette("coolwarm", len(sales_by_genre))
    text_color = "#FFFFFF" if theme == 'dark' else "#000000"

    sns.barplot(x='Genre', y='NA_Sales', data=sales_by_genre, palette=colors, ax=ax)

    ax.set_title('Vendas de Jogos por Gênero (NA)', fontsize=16, fontweight='bold', color=text_color)
    ax.set_xlabel('Gênero', fontsize=12, color=text_color)
    ax.set_ylabel('Vendas Totais na NA (Milhões)', fontsize=12, color=text_color)

    ax.tick_params(axis='y', labelcolor=text_color)

    for label in ax.get_xticklabels():
        label.set_rotation(45)  # Rotaciona em 45 graus
        label.set_horizontalalignment('right')  # Alinha à direita
        label.set_rotation_mode('anchor')  # Define o modo de rotação
        label.set_color(text_color)  # Define a cor do texto

    ax.grid(True, linestyle='--', alpha=0.7, color='#FFFFFF')

    if ax.get_legend():
        ax.get_legend().remove()

    plt.tight_layout()


def sales_per_genre_EU(df, ax, theme):
    sales_by_genre = df.groupby('Genre')['EU_Sales'].sum().reset_index()
    sales_by_genre = sales_by_genre.sort_values(by='EU_Sales', ascending=False)

    colors = sns.color_palette("coolwarm", len(sales_by_genre))
    text_color = "#FFFFFF" if theme == 'dark' else "#000000"

    sns.barplot(x='Genre', y='EU_Sales', data=sales_by_genre, palette=colors, ax=ax)

    ax.set_title('Vendas de Jogos por Gênero (EU)', fontsize=16, fontweight='bold', color=text_color)
    ax.set_xlabel('Gênero', fontsize=12, color=text_color)
    ax.set_ylabel('Vendas Totais na EU (Milhões)', fontsize=12, color=text_color)

    ax.tick_params(axis='x', rotation=45, labelcolor=text_color)
    ax.tick_params(axis='y', labelcolor=text_color)

    ax.grid(True, linestyle='--', alpha=0.7, color='#FFFFFF')

    if ax.get_legend():
        ax.get_legend().remove()

    plt.tight_layout()


def sales_per_genre_JP(df, ax, theme):
    sales_by_genre = df.groupby('Genre')['JP_Sales'].sum().reset_index()
    sales_by_genre = sales_by_genre.sort_values(by='JP_Sales', ascending=False)

    colors = sns.color_palette("coolwarm", len(sales_by_genre))
    text_color = "#FFFFFF" if theme == 'dark' else "#000000"

    sns.barplot(x='Genre', y='JP_Sales', data=sales_by_genre, palette=colors, ax=ax)

    ax.set_title('Vendas de Jogos por Gênero (JP)', fontsize=16, fontweight='bold', color=text_color)
    ax.set_xlabel('Gênero', fontsize=12, color=text_color)
    ax.set_ylabel('Vendas Totais no JP (Milhões)', fontsize=12, color=text_color)

    ax.tick_params(axis='x', rotation=45, labelcolor=text_color)
    ax.tick_params(axis='y', labelcolor=text_color)

    ax.grid(True, linestyle='--', alpha=0.7, color='#FFFFFF')

    if ax.get_legend():
        ax.get_legend().remove()

    plt.tight_layout()


def hist_sales_per_platform(df, ax, theme):
    df_grouped = df.groupby('Platform')['Global_Sales'].sum().reset_index()
    df_grouped = df_grouped.sort_values(by='Global_Sales', ascending=False).head(20)

    text_color = "#FFFFFF" if theme == 'dark' else "#000000"

    sns.histplot(data=df_grouped, x='Platform', weights='Global_Sales', color='#ff0008', ax=ax)

    ax.set_title('Histograma de Vendas por Plataforma', fontweight='bold', color=text_color)
    ax.set_xlabel('Plataforma', color=text_color)
    ax.set_ylabel('Vendas (bilhão)', color=text_color)
    ax.tick_params(axis='x', colors=text_color, rotation=90)
    ax.tick_params(axis='y', colors=text_color)

    ax.grid(True, linestyle='--', alpha=0.7, color='#FFFFFF')


def hist_sales_per_year(df, ax, theme):
    df_grouped = df.groupby('Year')['Global_Sales'].sum().reset_index()

    text_color = "#FFFFFF" if theme == 'dark' else "#000000"

    sns.histplot(data=df_grouped, x='Year', weights='Global_Sales', color='#65c7a6', bins=40, ax=ax)

    ax.set_title('Histograma de Vendas por Ano de Lançamento', fontweight='bold', color=text_color)
    ax.set_xlabel('Ano de Lançamento', color=text_color)
    ax.set_ylabel('Vendas (bilhão)', color=text_color)
    ax.tick_params(axis='x', colors=text_color)
    ax.tick_params(axis='y', colors=text_color)

    ax.grid(True, linestyle='--', alpha=0.7, color='#FFFFFF')


def sales_per_publisher_NA(df, ax, theme):
    sales_by_publisher = df.groupby('Publisher')['NA_Sales'].sum().reset_index()
    sales_by_publisher = sales_by_publisher.sort_values(by='NA_Sales', ascending=True).tail(20)

    colors = sns.color_palette("coolwarm", len(sales_by_publisher))
    text_color = "#FFFFFF" if theme == 'dark' else "#000000"

    sns.barplot(x='NA_Sales', y='Publisher', data=sales_by_publisher, palette=colors, ax=ax)

    ax.set_title('Vendas de Jogos por Publicadora (NA)', fontsize=16, fontweight='bold', color=text_color)
    ax.set_xlabel('Vendas Totais na NA (Milhões)', fontsize=12, color=text_color)
    ax.set_ylabel('Publicadora', fontsize=12, color=text_color)

    ax.tick_params(axis='y', labelcolor=text_color)
    ax.tick_params(axis='x', labelcolor=text_color)

    if ax.get_legend():
        ax.get_legend().remove()

    plt.tight_layout()


def sales_per_publisher_EU(df, ax, theme):
    sales_by_publisher = df.groupby('Publisher')['EU_Sales'].sum().reset_index()
    sales_by_publisher = sales_by_publisher.sort_values(by='EU_Sales', ascending=True).tail(20)

    colors = sns.color_palette("coolwarm", len(sales_by_publisher))
    text_color = "#FFFFFF" if theme == 'dark' else "#000000"

    sns.barplot(x='EU_Sales', y='Publisher', data=sales_by_publisher, palette=colors, ax=ax)

    ax.set_title('Vendas de Jogos por Publicadora (EU)', fontsize=16, fontweight='bold', color=text_color)
    ax.set_xlabel('Vendas Totais na EU (Milhões)', fontsize=12, color=text_color)
    ax.set_ylabel('Publicadora', fontsize=12, color=text_color)

    ax.tick_params(axis='y', labelcolor=text_color)
    ax.tick_params(axis='x', labelcolor=text_color)

    if ax.get_legend():
        ax.get_legend().remove()

    plt.tight_layout()


def sales_per_publisher_JP(df, ax, theme):
    sales_by_publisher = df.groupby('Publisher')['JP_Sales'].sum().reset_index()
    sales_by_publisher = sales_by_publisher.sort_values(by='JP_Sales', ascending=True).tail(20)

    colors = sns.color_palette("coolwarm", len(sales_by_publisher))
    text_color = "#FFFFFF" if theme == 'dark' else "#000000"

    sns.barplot(x='JP_Sales', y='Publisher', data=sales_by_publisher, palette=colors, ax=ax)

    ax.set_title('Vendas de Jogos por Publicadora (JP)', fontsize=16, fontweight='bold', color=text_color)
    ax.set_xlabel('Vendas Totais no JP (Milhões)', fontsize=12, color=text_color)
    ax.set_ylabel('Publicadora', fontsize=12, color=text_color)

    ax.tick_params(axis='y', labelcolor=text_color)
    ax.tick_params(axis='x', labelcolor=text_color)

    ax.grid(True, linestyle='--', alpha=0.7, color='#FFFFFF')

    if ax.get_legend():
        ax.get_legend().remove()

    plt.tight_layout()

