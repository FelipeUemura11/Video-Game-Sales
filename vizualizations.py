import base64
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from io import BytesIO


def mudar_cor_borda(ax, cor):
    for spine in ['top', 'right', 'bottom', 'left']:
        ax.spines[spine].set_color(cor)
        ax.spines[spine].set_linewidth(1)


def configurar_cores_e_estilos(theme):
    if theme == 'dark':
        sns.set_theme(style='darkgrid')
        background_color = (43 / 255, 48 / 255, 53 / 255, 0.0)
        text_color = "#FFFFFF"
        grid_color = '#FFFFFF'
    else:
        sns.set_theme(style='whitegrid')
        background_color = (1, 1, 1, 0.0)
        text_color = "#000000"
        grid_color = '#000000'
    return background_color, text_color, grid_color


def gerar_imagem(plot_function, df, theme):
    buffer = BytesIO()
    background_color, text_color, grid_color = configurar_cores_e_estilos(theme)

    fig, ax = plt.subplots(figsize=(12, 6), facecolor=background_color)
    ax.set_facecolor(background_color)

    plot_function(df, ax, text_color, grid_color)

    plt.savefig(buffer, format='png', bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close(fig)

    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()

    return f"data:image/png;base64,{img_base64}"


def generate_visualizations(df, theme):
    sns.set_theme(style='darkgrid' if theme == 'dark' else 'whitegrid')

    # Lista de funções de plotagem a serem chamadas
    plot_functions = [
        sales_per_platform,
        regional_sales,

        # Vendas por gênero por região
        lambda df, ax, tc, gc: sales_per_region_genre(df, ax, theme, 'NA', tc, gc),
        lambda df, ax, tc, gc: sales_per_region_genre(df, ax, theme, 'EU', tc, gc),
        lambda df, ax, tc, gc: sales_per_region_genre(df, ax, theme, 'JP', tc, gc),
        hist_sales_per_platform,
        hist_sales_per_year,

        # Vendas por publicadora por região
        lambda df, ax, tc, gc: sales_per_publisher(df, ax, theme, 'NA', tc, gc),
        lambda df, ax, tc, gc: sales_per_publisher(df, ax, theme, 'EU', tc, gc),
        lambda df, ax, tc, gc: sales_per_publisher(df, ax, theme, 'JP', tc, gc),
        genero_predominante_regiao
    ]

    visualizations = [{'imagem': gerar_imagem(plot_func, df, theme)} for plot_func in plot_functions]

    return visualizations


def sales_per_platform(df, ax, text_color, grid_color):
    sales_per_platform = df.groupby('Platform')['Global_Sales'].sum() / 1000
    sales_per_platform = sales_per_platform.reset_index()
    order = sales_per_platform.sort_values(by='Global_Sales', ascending=False)['Platform']

    sns.barplot(x='Platform', y='Global_Sales', data=sales_per_platform, order=order, color='#dc6fed', ax=ax)

    for patch in ax.patches:
        patch.set_edgecolor(grid_color)

    ax.set_title('Total de Vendas por Plataforma', fontweight='bold', color=text_color)
    ax.set_ylabel('Total de Vendas (em bilhão)', color=text_color)
    ax.set_xlabel('Plataforma', color=text_color)
    ax.tick_params(axis='x', colors=text_color, rotation=90)
    ax.tick_params(axis='y', colors=text_color)

    ax.grid(True, linestyle='--', alpha=0.7, color=grid_color)
    mudar_cor_borda(ax, grid_color)


def regional_sales(df, ax, text_color, grid_color):
    regional_sales = df[['NA_Sales', 'EU_Sales', 'JP_Sales']].sum() / 1000

    regional_sales.plot(kind='barh', color=['#9af252', '#edf252', '#e6844c'], ax=ax)

    for patch in ax.patches:
        patch.set_edgecolor(grid_color)

    ax.set_title('Vendas Totais de Jogos por Região', fontweight='bold', color=text_color)
    ax.set_xlabel('Total de Vendas (bilhões)', color=text_color)
    ax.set_ylabel('Região', rotation=0, color=text_color)
    ax.tick_params(axis='x', colors=text_color)
    ax.tick_params(axis='y', colors=text_color, rotation=45)

    ax.grid(True, linestyle='--', alpha=0.7, color=grid_color)
    mudar_cor_borda(ax, grid_color)


def sales_per_region_genre(df, ax, theme, region, text_color, grid_color):
    column = f'{region}_Sales'
    sales_by_genre = df.groupby('Genre')[column].sum().reset_index()
    sales_by_genre = sales_by_genre.sort_values(by=column, ascending=False)

    colors = sns.color_palette("coolwarm", len(sales_by_genre))

    sns.barplot(x='Genre', y=column, data=sales_by_genre, palette=colors, ax=ax)

    for patch in ax.patches:
        patch.set_edgecolor(grid_color)

    ax.set_title(f'Vendas de Jogos por Gênero ({region})', fontsize=16, fontweight='bold', color=text_color)
    ax.set_xlabel('Gênero', fontsize=12, color=text_color)
    ax.set_ylabel(f'Vendas Totais no {region} (Milhões)', fontsize=12, color=text_color)

    ax.tick_params(axis='x', rotation=45, labelcolor=text_color)
    ax.tick_params(axis='y', labelcolor=text_color)

    ax.grid(True, linestyle='--', alpha=0.7, color=grid_color)
    mudar_cor_borda(ax, grid_color)

    plt.tight_layout()


def hist_sales_per_platform(df, ax, text_color, grid_color):
    df_grouped = df.groupby('Platform')['Global_Sales'].sum().reset_index()
    df_grouped = df_grouped.sort_values(by='Global_Sales', ascending=False).head(20)

    sns.histplot(data=df_grouped, x='Platform', weights='Global_Sales', color='#ff0008', ax=ax)

    for patch in ax.patches:
        patch.set_edgecolor(grid_color)

    ax.set_title('Histograma de Vendas por Plataforma', fontweight='bold', color=text_color)
    ax.set_xlabel('Plataforma', color=text_color)
    ax.set_ylabel('Vendas (bilhão)', color=text_color)
    ax.tick_params(axis='x', colors=text_color, rotation=90)
    ax.tick_params(axis='y', colors=text_color)

    ax.grid(True, linestyle='--', alpha=0.7, color=grid_color)
    mudar_cor_borda(ax, grid_color)


def hist_sales_per_year(df, ax, text_color, grid_color):
    df_grouped = df.groupby('Year')['Global_Sales'].sum().reset_index()

    sns.histplot(data=df_grouped, x='Year', weights='Global_Sales', color='#65c7a6', bins=40, ax=ax)

    for patch in ax.patches:
        patch.set_edgecolor(grid_color)

    ax.set_title('Histograma de Vendas por Ano de Lançamento', fontweight='bold', color=text_color)
    ax.set_xlabel('Ano de Lançamento', color=text_color)
    ax.set_ylabel('Vendas (bilhão)', color=text_color)
    ax.tick_params(axis='x', colors=text_color)
    ax.tick_params(axis='y', colors=text_color)

    ax.grid(True, linestyle='--', alpha=0.7, color=grid_color)
    mudar_cor_borda(ax, grid_color)


def sales_per_publisher(df, ax, theme, region, text_color, grid_color):
    column = f'{region}_Sales'
    sales_by_publisher = df.groupby('Publisher')[column].sum().reset_index()
    sales_by_publisher = sales_by_publisher.sort_values(by=column, ascending=True).tail(20)

    colors = sns.color_palette("coolwarm", len(sales_by_publisher))

    sns.barplot(x=column, y='Publisher', data=sales_by_publisher, palette=colors, ax=ax)

    for patch in ax.patches:
        patch.set_edgecolor(grid_color)

    ax.set_title(f'Vendas de Jogos por Publicadora ({region})', fontsize=16, fontweight='bold', color=text_color)
    ax.set_xlabel(f'Vendas Totais no {region} (Milhões)', fontsize=12, color=text_color)
    ax.set_ylabel('Publicadora', fontsize=12, color=text_color)

    ax.tick_params(axis='y', labelcolor=text_color)
    ax.tick_params(axis='x', labelcolor=text_color)

    if ax.get_legend():
        ax.get_legend().remove()

    mudar_cor_borda(ax, grid_color)
    plt.tight_layout()


def genero_predominante_regiao(df, ax, text_color, grid_color):
    valores_por_regiao = df.groupby('Genre')[['NA_Sales', 'EU_Sales', 'JP_Sales']].sum().reset_index()
    valores_por_regiao_normalizado = valores_por_regiao.set_index('Genre').apply(lambda x: x / x.sum(), axis=0)

    colors = sns.color_palette("Set2", len(valores_por_regiao_normalizado))

    valores_por_regiao_normalizado.plot(
        kind='bar',
        stacked=False,
        figsize=(10, 6),
        color=colors,
        ax=ax
    )

    for patch in ax.patches:
        patch.set_edgecolor(grid_color)

    ax.set_title('Gêneros Mais Predominantes por Região', fontweight='bold', color=text_color)
    ax.set_xlabel('Gênero', color=text_color)
    ax.set_ylabel('Proporção de Vendas', color=text_color)
    ax.tick_params(axis='x', rotation=45, colors=text_color)
    ax.tick_params(axis='y', colors=text_color)
    ax.legend(title='Região', loc='upper left', fontsize=10, title_fontsize=12, facecolor='white')

    ax.grid(True, linestyle='--', alpha=0.7, color=grid_color)
    mudar_cor_borda(ax, grid_color)


def gerar_plot_interativo(df, theme):
    sales_over_time = df.groupby('Year')['Global_Sales'].sum().reset_index()

    line_color = 'blue' if theme == 'light' else '#FFFF12'

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=sales_over_time['Year'],
        y=sales_over_time['Global_Sales'],
        mode='lines+markers',
        marker=dict(size=6, color=line_color),
        line=dict(width=2, color=line_color, dash='solid')
    ))

    text_color = '#FFFFFF' if theme == 'dark' else '#000000'
    grid_color = '#000000' if theme == 'light' else '#FFFFFF'
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
