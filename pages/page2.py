import dash
import dash_bootstrap_components as dbc
from app import *
import pandas as pd
import plotly_express as px
from dash import html, dcc, Input, Output, State
import base64
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.subplots as sp


'''=============================== Carregar os dados #==============================='''
df = pd.read_csv('/home/black_d/Downloads/Provas/data/df_tendências_de_compras.csv')


''' ============================# config_style #================================'''
tab_card = {'height':'100%'}

main_config = {
    "margin": {"l": 10, "r": 10, "t": 10, "b": 10}, 
    "plot_bgcolor": "rgba(0,0,0,0)",  # Transparência no fundo do gráfico
    "paper_bgcolor": "rgba(0,0,0,0)",  # Transparência no fundo da área do gráfico
    "font": {"color": "white", "size": 15},  # Fonte branca tamanho 15
}
config_graph={"displayModeBar": False, "showTips": False}

''' ============================#           #================================'''


# Layout do aplicativo
layout = html.Div([
    # # sidebar,
    # html.Div([
    #     html.H3('Tendências de Comportamento de Compras', style={"textAlign": "center"}),
    #     dash.page_container
    # ], className="content"),

    # Container com os gráficos
    dbc.Container([
        # 1 Row
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dbc.Row(
                            dbc.Col(
                                html.H4('Vendas por Tamanho e Temporada')
                            )
                        ), 
                        dbc.Row([
                            dbc.Col([
                                dcc.Graph(id='graph1', className='dbc', config=config_graph, 
                                          style = {'width':'100%'})
                            ], sm=12, md=12)
                        ])
                    ])
                ], style=tab_card)
            ], sm=12, lg=6, ), 
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dbc.Row(
                            dbc.Col(
                                html.H4('Cores mais Utilizadas por Temporada')
                            )
                        ),
                        dbc.Row([
                            dbc.Col([
                                dcc.Graph(id='graph2', className='dbc',
                                          config=config_graph, 
                                          style={'height': '100%'})
                            ], sm=12, md=12, style={'width': '100%'})
                        ])
                    ])
                ], style=tab_card)
            ], sm=12, lg=6, )
        ], className = 'mb-3'),
        # 2 Row
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dbc.Row(
                            dbc.Col(
                                html.H4('Avaliações por Categoria e Localização')
                            )
                        ),
                        dbc.Row([
                            dbc.Col([
                                dcc.Graph(id = 'graph3', className = 'dbc', config = config_graph)
                            ])
                        ])
                    ])
                ], style=tab_card)
            ], sm=12, lg=6), 
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dbc.Row(
                            dbc.Col(
                                html.H4('Pagamentos por Categoria e Produto')
                            )
                        ),
                        dbc.Row([
                            dbc.Col([
                                dcc.Graph(id = 'graph4', className = 'dbc', config = config_graph)
                            ])
                        ])
                    ])
                ], style=tab_card)
            ], sm=12, lg=6)
        ], className = 'mb-3'), 
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dbc.Row(
                            dbc.Col(
                                html.H4('Compras de Clientes com e sem Desconto')
                            )
                        ), 
                        dbc.Row([
                            dbc.Col([
                                dcc.Graph(id = 'graph5', className = 'dbc', config = config_graph, 
                                          style = { 
                                                   'margin-bottom':'-25px', 
                                                   
                                                   }
                                                   )
                            ])
                        ])
                    ])
                ], style = tab_card)
            ], sm=12, lg=12)
        ])
    ], fluid=True,  style={'height':'100vh', 'margin-top':'7px'})
])

# '''=======================# graficos-1 #==========================='''
def vendas_por_tamanho_e_temporada(df):
    # Relação das Vendas por Tamanho e Temporadas
    tamanho_por_temporada = df.groupby(['Temporada', 'Tamanho'], observed=False)['Valor_da_compra_(USD)'].sum().reset_index()  

    # Criando o gráfico de treemap com as cores definidas para a temporada e tamanho
    fig = px.treemap(tamanho_por_temporada, 
                    path=['Temporada', 'Tamanho'], 
                    values='Valor_da_compra_(USD)',  
                    color='Valor_da_compra_(USD)',  
                    color_continuous_scale='ice', 
                                        # color_continuous_scale='RdBu'  

    )

    fig.update_layout(
        main_config, 
        height=300,  
        showlegend=False,  # Removendo a legenda
        coloraxis_showscale=False  # Removendo a barra de cor
    )

    return fig

# '''=======================# graficos-2 #==========================='''
def cores_por_temporada(df):
    # Contar a frequência de cada cor por temporada
    df_colors = df.groupby(["Temporada", "Cor"], observed = False).size().reset_index(name="Contagem")

    # Encontrar a(s) cor(es) mais usada(s) por temporada
    max_counts = df_colors.groupby("Temporada", observed = False)["Contagem"].transform('max')
    df_top_colors = df_colors[df_colors["Contagem"] == max_counts]

    # Ordem personalizada das estações
    estacoes_ordem = ["Primavera", "Verão", "Outono", "Inverno"]

    # Criar um subplot com 1 linha e várias colunas (uma para cada temporada)
    fig = sp.make_subplots(
        rows=1, cols=4,  # Uma linha com 4 gráficos
        subplot_titles=estacoes_ordem,
        specs=[[{'type': 'pie'}, {'type': 'pie'}, {'type': 'pie'}, {'type': 'pie'}]],   # Gráficos de pizza
    )

    # Iterar pelas estações e adicionar gráficos de pizza
    for i, estacao in enumerate(estacoes_ordem):
        # Filtrar dados para a estação específica
        df_estacao = df_top_colors[df_top_colors["Temporada"] == estacao]
        
        # Criar o gráfico de pizza para a estação
        fig.add_trace(
            go.Pie(
                labels=df_estacao["Cor"], 
                values=df_estacao["Contagem"],
                name=estacao,
                textinfo="label",
                marker=dict(
                    colors=df_estacao["Cor"]  # Usar a cor correspondente para cada fatia
                ), 
            ),
            row=1, col=i+1  # Posicionar o gráfico de pizza na coluna correspondente
        )

    # Adicionar imagem de fundo
    fig.add_layout_image(
        dict(
            source='assets/___5_-removebg-preview.png',  # Caminho relativo da imagem
            xref="paper", yref="paper",  # Referência para a área do papel (escala completa do gráfico)
            x=0, y=1,  # Posição da imagem
            sizex=1.01, sizey=1.30, 
            xanchor="left", yanchor="top",
            opacity=1,  # Opacidade
            layer="below"  # Coloca a imagem abaixo dos gráficos
        )
    )

    # Ajustar o layout
    fig.update_layout(
        main_config, 
        showlegend=False,
        height=300,
        margin={"l": 0, "r": 0, "t": 0, "b": 0},   
        font=dict(weight='bold', family='Arial',), 
        autosize=True,  
    )
    # Ajustar as posições dos títulos das estações no eixo Y (mais para baixo)
    fig.update_annotations(
        y=0.75  # Ajuste para mover os títulos para baixo
    )

    return fig

# '''=======================# graficos-3 #==========================='''
def avaliacao_por_categoria_e_localizacao(df):
    def menores_avaliacoes():
        # Agrupar por categoria e item, pegando a menor avaliação
        avaliacao_de_categoria_e_item = df.groupby(['Categoria', 'Item_comprado', 'Localização'])['Avaliação_da_avaliação'].min().reset_index()
        menor_avaliacao_por_categoria = avaliacao_de_categoria_e_item.groupby('Categoria')['Avaliação_da_avaliação'].min().reset_index()
        menores_avaliacoes = pd.merge(avaliacao_de_categoria_e_item, menor_avaliacao_por_categoria, 
                                    on=['Categoria', 'Avaliação_da_avaliação'])
        return menores_avaliacoes
    
    def maiores_avaliacoes():
        # Agrupar por categoria e item, pegando a maior avaliação
        avaliacao_de_categoria_e_item = df.groupby(['Categoria', 'Item_comprado', 'Localização'])['Avaliação_da_avaliação'].max().reset_index()
        maior_avaliacao_por_categoria = avaliacao_de_categoria_e_item.groupby('Categoria')['Avaliação_da_avaliação'].max().reset_index()
        maiores_avaliacoes = pd.merge(avaliacao_de_categoria_e_item, maior_avaliacao_por_categoria, 
                                    on=['Categoria', 'Avaliação_da_avaliação'])
        return maiores_avaliacoes

    # Criando o gráfico Sunburst
    fig1 = px.sunburst(menores_avaliacoes(),
                    path=['Categoria', 'Item_comprado', 'Localização'], 
                    values='Avaliação_da_avaliação', 
                    title='Menores Avaliações por Categoria, Item e Localidade',
                    color='Categoria',  # Aplica coloração baseada nos valores da avaliação
                    # color_discrete_sequence=px.colors.sequential.speed_r
                    color_discrete_sequence=['green', 'olive', 'silver', '#1F77B4']

                    )

    fig2 = px.sunburst(maiores_avaliacoes(), 
                    path=['Categoria', 'Item_comprado', 'Localização'], 
                    values='Avaliação_da_avaliação', 
                    title='Maiores Avaliações por Categoria, Item e Cidade', 
                    color_continuous_scale='ice'
                    )

    # Criando o layout de subplots
    fig = make_subplots(
        rows=1, cols=2, 
        specs=[[{'type': 'sunburst'}, {'type': 'sunburst'}]],
        subplot_titles=['Menores Avaliações', 'Maiores Avaliações']
    )

    # Ajustando a posição dos títulos no eixo Y
    fig.update_layout(
        annotations=[
            dict(
                x=0.24,  # Ajusta a posição no eixo X (subgráfico 1)
                y=0.98,  # Ajusta a posição no eixo Y (subgráfico 1)
                text='Menores Avaliações',
                showarrow=False,
                font=dict(size=15, color='white'),
                xref='paper', yref='paper'
            ),
            dict(
                x=0.75,  # Ajusta a posição no eixo X (subgráfico 2)
                y=0.98,  # Ajusta a posição no eixo Y (subgráfico 2)
                text='Maiores Avaliações',
                showarrow=False,
                font=dict(size=15, color='white'),
                xref='paper', yref='paper'
            )
        ]
    )

    # Adicionando os gráficos Sunburst nas subplots
    for trace in fig1.data:
        fig.add_trace(trace, row=1, col=1)

    for trace in fig2.data:
        fig.add_trace(trace, row=1, col=2)

    # Atualizando o layout dos gráficos
    fig.update_traces(marker=dict(line=dict(width=1.5, color='black')))  # Adiciona uma borda preta
    fig.update_layout(
        main_config, 
        showlegend=False,
        height = 300, 
    )

    return fig

# '''=======================# graficos-4 #==========================='''
def Pagamentos_por_Categoria_e_Produto(df):

    def metodo_de_pagamento_por_categoria():
        # Agrupar por Categoria do Produto e Método de Pagamento e contar a quantidade
        metodo_pagamento_por_categoria = df.groupby(['Categoria', 'Método_de_pagamento']).size().reset_index(name='Quantidade')

        sort_metodo_pagamento_por_categoria = metodo_pagamento_por_categoria.sort_values(by = 'Quantidade', ascending = False)

        return sort_metodo_pagamento_por_categoria

    fig_categoria = px.bar(metodo_de_pagamento_por_categoria(), 
                        x='Categoria', 
                        y='Quantidade', 
                        color='Método_de_pagamento', 
                        color_discrete_sequence=['#1F77B4', 'green', 'silver', 'olive',  '#FF7F0E', '#D62728']


                        #    text = 'Quantidade',['#1F77B4', '#2CA02C', '#FF7F0E', '#D62728', 'silver', 'olive']
                        )

    # Configurar para mostrar as barras lado a lado
    fig_categoria.update_layout(
        main_config, 
        height = 250, 
        barmode='group',
        yaxis=dict(showticklabels=True, 
                    visible=True,
                    showgrid=False,  # Remove a linha de grade do eixo y
                    zeroline=True
                            
                   ),  
        legend = dict(
            title = 'Pagamentos', 
            font = dict(size=13)
        )
        ) 
    
    return fig_categoria

# '''=======================# graficos-4 #==========================='''
def clientes_com_e_sem_desconto(df):

    def separar_por_desconto(df):
        # Criando o DataFrame agrupado dentro da função
        df_frequencia_de_compras_por_desconto = df.groupby(['Desconto_aplicado', 'Frequência_de_compras']).size().reset_index(name='Quantidade')

        # Separando os clientes que utilizam e não utilizam desconto
        nao_utilizam = df_frequencia_de_compras_por_desconto[df_frequencia_de_compras_por_desconto['Desconto_aplicado'] == 'No']
        utilizam = df_frequencia_de_compras_por_desconto[df_frequencia_de_compras_por_desconto['Desconto_aplicado'] == 'Yes']
        
        return nao_utilizam, utilizam

    # Agora podemos chamar a função diretamente com o DataFrame original:
    nao_utilizam, utilizam = separar_por_desconto(df)

    # Define a função para ajustar textposition dinamicamente
    def ajustar_textposition(y_values):
        return ["bottom center" if y < 130 else "bottom center" if y > 255 else "middle center" for y in y_values]

    # Criação do gráfico único
    fig = go.Figure()

    # Gráfico 1: Clientes com Desconto
    fig.add_trace(
        go.Scatter(
            x=utilizam["Frequência_de_compras"],
            y=utilizam["Quantidade"],
            mode='lines+markers+text',  # Adiciona linha, pontos e texto
            line=dict(color="green"),  # Cor da linha
            name="Com Desconto",  # Nome da série
            text=utilizam["Quantidade"],  # Adiciona os valores como texto
            textposition=ajustar_textposition(utilizam["Quantidade"]),  
            hoverinfo="text+x+y",  # Exibe as informações no hover (texto, eixo X e eixo Y)
        )
    )

    # Gráfico 2: Clientes sem Desconto
    fig.add_trace(
        go.Scatter(
            x=nao_utilizam["Frequência_de_compras"],
            y=nao_utilizam["Quantidade"],
            mode='lines+markers+text',  # Adiciona linha, pontos e texto
            line=dict(color="#1F77B4"),  # Cor da linha
            name="Sem Desconto",  # Nome da série
            text=nao_utilizam["Quantidade"],  # Adiciona os valores como texto
            textposition=ajustar_textposition(nao_utilizam["Quantidade"]),  
            hoverinfo="text+x+y",  # Exibe as informações no hover (texto, eixo X e eixo Y)
        )
    )

    # Layout do gráfico
    fig.update_layout(
        main_config, 
        showlegend=True,  # Exibe a legenda
        height = 300, 
        # automargin=True,
        xaxis=dict(
            title_text="",
            showgrid=False,  # Remove a linha de grade do eixo x
            zeroline=True,  # Remove a linha zero do eixo x
            showticklabels=True, 
            # tickangle=45
            
        ),
        yaxis=dict(
            # title_standoff=5,
            title_text="",
            showgrid=True,  # Remove a linha de grade do eixo y
            zeroline=True,  # Remove a linha zero do eixo y
            showticklabels=False, 
            gridwidth=0.01, 
            gridcolor="gray", 
        ), 
    )

    # Ajusta os eixos X para melhor visualização
    fig.update_xaxes(title_text="Frequência de Compras", tickangle=30)

    # Ajusta os eixos Y
    fig.update_yaxes(title_text="Quantidade")

    return fig


'''=======================# callBacks #==========================='''
@app.callback(
    
    Output('graph1', 'figure'),
    Output('graph2', 'figure'),
    Output('graph3', 'figure'),
    Output('graph4', 'figure'), 
    Output('graph5', 'figure'), 

    [
        Input("gender-all", "n_clicks"),
        Input("gender-male", "n_clicks"),
        Input("gender-female", "n_clicks")
    ]
)
def update_graphs(n_clicks_all, n_clicks_male, n_clicks_female):
    ctx = dash.callback_context
    if not ctx.triggered:
        gender_filter = 'All'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == "gender-all":
            gender_filter = 'All'
        elif button_id == "gender-male":
            gender_filter = 'Masculino'
        elif button_id == "gender-female":
            gender_filter = 'Feminino'

    # Filtrar o dataframe com base no gênero
    filtered_df = df if gender_filter == 'All' else df[df['Gênero'] == gender_filter]

    #criando graficos
    graph1 = vendas_por_tamanho_e_temporada(filtered_df)
    graph2 = cores_por_temporada(filtered_df)
    graph3 = avaliacao_por_categoria_e_localizacao(filtered_df)
    graph4 = Pagamentos_por_Categoria_e_Produto(filtered_df)
    graph5 = clientes_com_e_sem_desconto(filtered_df)

    return(
        graph1, 
        graph2, 
        graph3, 
        graph4, 
        graph5
    )


if __name__ == "__main__":
    app.run_server(debug=True)
