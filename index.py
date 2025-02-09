import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash_bootstrap_templates import ThemeSwitchAIO
from app import *
import os



'''=============================== Carregar os dados #==============================='''
# Caminho relativo para a pasta "data"
file_path = os.path.join(os.path.dirname(__file__), "data", "df_tendências_de_compras.csv")

if not os.path.exists(file_path):
    import requests
    url =  'https://github.com/saulloabreu/tendencia_de_compras/blob/main/data/df_tend%C3%AAncias_de_compras.csv'
    r = requests.get(url)
    os.makedirs("data", exist_ok = True)
    with open(file_path, "wb") as f:
        f.write(r.content)

# Carregando o arquivo
df = pd.read_csv(file_path)


''' ============================# config_style #================================'''
tab_card = {'height':'100%'}

main_config = {
    "margin": {"l": 10, "r": 10, "t": 10, "b": 10}, 
    "plot_bgcolor": "rgba(0,0,0,0)",  # Transparência no fundo do gráfico
    "paper_bgcolor": "rgba(0,0,0,0)",  # Transparência no fundo da área do gráfico
    "font": {"color": "white", "size": 15},  # Fonte branca tamanho 15
}

config_graph={"displayModeBar": False, "showTips": False}


''' ============================# Sidebar #================================'''
sidebar_header = dbc.Row(
    [
        dbc.Col(html.H4("Tendências \nde Compras", className="display-7")),
        dbc.Col(
            [
                html.Button(
                    # use the Bootstrap navbar-toggler classes to style
                    html.Span(className="navbar-toggler-icon"),
                    className="navbar-toggler",
                    # the navbar-toggler classes don't set color
                    style={
                        "color": "rgba(0,0,0,.5)",
                        "border-color": "rgba(0,0,0,.1)",
                    },
                    id="navbar-toggle",
                ),
                html.Button(
                    # use the Bootstrap navbar-toggler classes to style
                    html.Span(className="navbar-toggler-icon"),
                    className="navbar-toggler",
                    # the navbar-toggler classes don't set color
                    style={
                        "color": "rgba(0,0,0,.5)",
                        "border-color": "rgba(0,0,0,.1)",
                    },
                    id="sidebar-toggle",
                ),
            ],
            # the column containing the toggle will be only as wide as the
            # toggle, resulting in the toggle being right aligned
            width="auto",
            # vertically align the toggle in the center
            align="center",
        ),
    ]
)

sidebar = html.Div(
    [
        sidebar_header,
       # envolvemos a regra horizontal e a sinopse curta em uma div que pode ser
        # escondido em uma tela pequena
        html.Div(
            [
                html.Hr(),
                html.P(
                    "",
                    className="lead",
                ),
            ],
            id="blurb",
        ),
        # use o componente Collapse para animar links ocultos/revelados
       # Menu suspenso de painéis

        html.Div([
            dbc.NavLink([
                    html.Img(
                        src="https://i.pinimg.com/originals/1f/1c/55/1f1c55442e45f24420754ce64351f6c0.png",
                        style={"width": "30px", "height": "30px", "margin-right": "17px", "margin-bottom": "30px",},
                    ),
                    html.Span("DashBoards", 
                              className="nav-text", 
                              style={'font-size': '15px', "margin-bottom": "30px",})
                ],
                href="#",
                id="toggle-dropdown",  # ID para callback
                className="nav-link",
                style={
                    "display": "flex",
                    "align-items": "center",
                    "justify-content": "flex-start",
                    "padding": "0px",
                    "margin-bottom": "10px",
                },
            ),
            dbc.Collapse(
                dbc.ButtonGroup([
                       dbc.Button("DashBoard 1", href="/", color="info",className="m-1 btn-hover", 
                                    style = {'font-size': '12px'},
                                    ),
                        dbc.Button("DashBoard 2", id = 'btn-page2', href="/page2", color="info", className="m-1 btn-hover", 
                                   style = {'font-size': '12px'},
                                   ),
                    ], 
                    style = {'margin-top':'-35px'},
                    vertical=True,  # Exibe os botões na vertical
                    className="w-100",  # Faz o grupo ocupar 100% da largura
                ),
                id="dropdown-content",
            ),
        ]),
        # Dropdown de Filtro por Gênero
        html.Div([
            dbc.NavLink([
                    html.Img(
                        src="https://cdn-icons-png.flaticon.com/512/6488/6488674.png",
                        style={"width": "30px", "height": "30px", "margin-right": "10px"},
                    ),
                    html.Span("Filtrar por Gênero", className="nav-text", 
                                style={'font-size': '15px', "margin-left": "10px"})
                ],
                href="#",
                id="toggle-filter-dropdown",  # ID para callback
                className="nav-link",
                style={
                    "display": "flex",
                    "align-items": "center",
                    "justify-content": "flex-start",
                    "padding": "0px",
                },
            ),
            
            dbc.Collapse(
                html.Div(
                    dbc.ButtonGroup([
                             dcc.Store(id='selected-filter', storage_type='session'), #armazena a opção de filtro

                            dbc.Button("Todos", id="gender-all", href="#", color="info", className="m-1 btn-hover", style = {'font-size': '12px'}
                            ),
                            dbc.Button("Masculino", id="gender-male", href="#", color="info", className="m-1 btn-hover", style = {'font-size': '12px'}
                            ),
                            dbc.Button("Feminino", id="gender-female", href="#", color="info", className="m-1 btn-hover", style = {'font-size': '12px'}
                            ),
                        ],
                        vertical=True,  # Exibe os botões na vertical
                        className="w-100",  # Faz o grupo ocupar 100% da largura
                    ),
                    style={
                        "padding": "5px",
                        "border-radius": "5px",  # Bordas arredondadas
                        'color': 'blue',  # Cor do texto
                    },
                ),
                id="filter-dropdown-content",
                is_open=False,  # Mantém sempre aberto
            ),

        ]),

    ],
    id="sidebar",
)

content = html.Div(id="page-content")

app.layout = html.Div([dcc.Location(id="url", refresh=True), sidebar, content], 
                          style={"height": "100vh", "overflow-x": "hidden"} 
)


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])

#layout do Dashboard
def render_page_content(pathname):
    if pathname == "/":
        html.Div([
        html.H3('Tendências de Comportamento de Compras', style={"textAlign": "center"}),
        dash.page_container
    ], className="content"),
        return dbc.Container(children=[
            # Layout
            # Row 1
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row(
                                dbc.Col(
                                    html.H5('Distribuição por Gênero'), 
                                    style={'textAlign': 'center'}
                                )
                            ),
                            dbc.Row([
                                dbc.Col([
                                    dcc.Graph(id='graph_2', className='dbc', config=config_graph, 
                                              style={'display': 'flex', 
                                                     'justify-content': 'center' ,
                                                     'width': '100%', 
                                                        }
                                                     )
                                ], sm=12, md=12, ), 
                            ], justify="center")
                        ])
                    ], style=tab_card)
                ], sm=12, lg=2),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row(
                                dbc.Col(
                                    html.H5('Top 10 Idades mais Frequentes')
                                )
                            ),
                            dbc.Row([
                                dbc.Col([
                                    dcc.Graph(id='graph_1', className='dbc', config=config_graph)
                                ], sm=12, md=12), 
                            ])
                        ])
                    ], style=tab_card)
                ], sm=12, lg=4),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row(
                                dbc.Col(
                                    html.H5('Maiores Receitas por Categorias'), 
                                    style={'textAlign': 'center'}
                                )
                            ),
                            dbc.Row([
                                dbc.Col([
                                    dcc.Graph(id='graph_7', className='dbc', config=config_graph, 
                                              style={'display': 'flex', 
                                                     'justify-content': 'center' ,
                                                     'width': '100%', 
                                                    #  'min-height': '300px', 
                                                        }
                                                     )
                                ], sm=12, md=12, ), 
                            ], justify="center")
                        ])
                    ], style=tab_card)
                ], sm=12, lg=2),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row(
                                dbc.Col(
                                    html.H5('Roupas com Mair Demanda por Temporada'),
                                )
                            ),
                            dbc.Row([
                                dbc.Col([
                                    dcc.Graph(id='graph_6', className='dbc', config=config_graph)
                                ], sm=12, lg=12, 
                                )
                            ]),
                        ])
                    ], style=tab_card)
                ], sm=12, lg=4)
            ], className='g-2 my-auto', style={'margin-top': '7px'}),
            # Row 2
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    dbc.Row(
                                        dbc.Col(
                                            html.H5('Método de Pagamentos mais Utilizados '),
                                        )
                                    ),
                                    dcc.Graph(id='graph_5', className='dbc', config=config_graph)
                                ])
                            ], style=tab_card)
                        ])
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    dbc.Row(
                                        dbc.Col(
                                            html.H5('Distribuição de Tamanho por Localizaçlão'),
                                        )
                                    ),
                                    dcc.Graph(id='graph_4', className='dbc', config=config_graph)
                                ])
                            ], style=tab_card)
                        ])
                    ], className='g-2 my-auto', style={'margin-top': '7px'})
                ], sm=12, lg=7),
                dbc.Col([
                    dbc.Card([
                        dbc.Row(
                            dbc.Col(
                                html.H5('Valor de Compra por Temporada', 
                                        style={"margin-top": "15px", "margin-left": "15px"}
                                        ),
                            )
                        ),
                        dcc.Graph(id='graph_3', className='dbc', config=config_graph, 
                        # style={"margin-top": "auto"}
                        )
                    ], style=tab_card)
                ], sm=12, lg=5)
            ], className='g-2 my-auto', style={'margin-top': '7px'}),



        ], fluid=True, style={'height': '-40vh'})
    
    elif pathname == '/page2':
            from pages import page2
            return page2.layout
    else:
        return "404 Page Error! Please select a valid page."


'''============================# Gráfico 1 #==================================='''
def distribuicao_idade(df):
    df_idade = df['Idade'].value_counts(ascending=False).reset_index(name='Quantidade_Clientes')
    df_idade = df_idade.head(10).sort_values(by='Quantidade_Clientes', ascending=True)

    df_idade_str = df_idade
    df_idade_str['Idade'] = df_idade['Idade'].astype(str)

    fig1 = px.bar(
        df_idade_str, 
        x='Quantidade_Clientes', 
        y='Idade', 
        color='Idade',  
        orientation='h', 
        text = 'Quantidade_Clientes',
        color_discrete_sequence = px.colors.sequential.Cividis_r
    )
    fig1.update_layout(
        main_config,
        height = 250,
        showlegend=False, 
        xaxis=dict(
            title = 'Quantidade de Clientes',
            showgrid=False,  # Remove a linha de grade do eixo x
            zeroline=False,  # Remove a linha zero do eixo x
            showticklabels=False
        ),
        yaxis=dict(
            showgrid=False,  # Remove a linha de grade do eixo y
            zeroline=False,  # Remove a linha zero do eixo y
            showticklabels=True
        )
    )
    return fig1

'''============================# Gráfico 2 #==================================='''
def distribuicao_genero(df, gender_filter):
    # Gráfico 2: Distribuição de Gênero nas Idades mais Frequentes
    distribuicao_por_genero = df.groupby('Gênero')['Idade'].count().reset_index()
    distribuicao_por_genero.columns = ['Gênero', 'Quantidade_Clientes']

    # Definir a cor dinamicamente com base no filtro
    color_map = {'Feminino': '#2C6A8C', 'Masculino': '#00224E'}
    
    if gender_filter in color_map:
        colors = [color_map[gender_filter]]
    else:
        colors = ['#2C6A8C', '#00224E']  # Mantém as duas cores se não houver filtro

    fig2 = go.Figure(data=[go.Pie(
        labels=distribuicao_por_genero['Gênero'],
        values=distribuicao_por_genero['Quantidade_Clientes'],
        marker=dict(colors=colors),  
        hole=0.4
    )])

    fig2.update_traces(hovertemplate="<b>%{label}</b><br>Valor: %{value}<br>Percentual: %{percent}", 
                       marker = dict(line=dict(color='#303030', width=3))
                       )
    fig2.update_layout(
        main_config,
        height=250,   
        legend=dict(
            orientation="h",
            y=-0.2
        ), 
        margin=dict(l=20, r=20, t=5, b=5),
    )

    return fig2


'''============================# Gráfico 3 #==================================='''
def compras_por_temporada(df):
    # Definindo a ordem correta das estações
    ordem_temporadas = ['Verão', 'Outono', 'Inverno', 'Primavera']

    # Garantindo que a coluna 'Temporada' tenha a ordem correta
    df['Temporada'] = pd.Categorical(df['Temporada'], categories=ordem_temporadas, ordered=True)

    # Agrupando dados por temporada, item e valor
    item_mais_vendido_por_temporada = df.groupby('Temporada', observed=False)['Valor_da_compra_(USD)'].sum().reset_index()

    # Ordenando os dados pela temporada (já ordenada de acordo com a ordem definida)
    item_mais_vendido_por_temporada = item_mais_vendido_por_temporada.sort_values(by='Temporada')

    # Criação de gráfico de barras
    bar = go.Bar(
        x=item_mais_vendido_por_temporada['Temporada'],
        y=item_mais_vendido_por_temporada['Valor_da_compra_(USD)'],
        name='Valor da Compra',
        marker=dict(color=px.colors.sequential.Cividis_r[9]),
        text=item_mais_vendido_por_temporada['Valor_da_compra_(USD)'],
    )

    # Criação de linha de tendência
    line = go.Scatter(
        x=item_mais_vendido_por_temporada['Temporada'],
        y=item_mais_vendido_por_temporada['Valor_da_compra_(USD)'],
        mode='lines+markers',  # Marcadores para os pontos da linha
        name='Linha de Tendência',
        line=dict(color='red', width=3)  # Definindo a cor e o estilo da linha
    )

    # Configuração do layout do gráfico
    layout = go.Layout(
        xaxis=dict(title='Temporada'),
        yaxis=dict(title='Valor de Compra (USD)'),
        showlegend=False
    )

    # Criando o gráfico
    fig3 = go.Figure(data=[bar, line], layout=layout)

    # Personalizando o layout
    fig3.update_layout( 
        main_config, 
        height=450, 
        xaxis=dict(
            showgrid=False,  # Remove a linha de grade do eixo x
            zeroline=False,  # Remove a linha zero do eixo x
            showticklabels=True, 
            tickangle=45, 
            showline=True, 
            linecolor='gray',  # Cor da linha (vermelho com opacidade)
            linewidth=2
        ),
        yaxis=dict(
            showgrid=False,  # Remove a linha de grade do eixo y
            zeroline=False,  # Remove a linha zero do eixo y
            showticklabels=False
        )
    )
    
    return fig3

'''============================# Gráfico 4 #==================================='''
def distribuicao_por_tamanho(df):
    # Distribuição de Tamanhos por Localização
    tamanho_por_local = df.groupby(['Localização', 'Tamanho']).size().reset_index(name='Quantidade')

    sort_tamanho_por_local = tamanho_por_local.sort_values(by = 'Quantidade', ascending = False)

    fig4 = px.bar(
        sort_tamanho_por_local, 
        x='Localização', 
        y='Quantidade', 
        color='Tamanho', 
        labels={'Quantidade': 'Quantidade', 'Localização': 'Localização', 'Tamanho': 'Tamanho'},
        color_discrete_sequence = [
            px.colors.sequential.Cividis_r[9], 
            px.colors.sequential.Cividis_r[4],
            px.colors.sequential.Cividis_r[7], 
            px.colors.sequential.Cividis_r[1], 
        ]

    )
    fig4.update_layout(  
                    main_config, 
                    height = 250, 
                        xaxis=dict(
                            showgrid=False,  # Remove a linha de grade do eixo x
                            zeroline=False,  # Remove a linha zero do eixo x
                            showticklabels=True, 
                            tickangle=45, 
                        ),
                        yaxis=dict(
                            showgrid=False,  # Remove a linha de grade do eixo y
                            zeroline=False,  # Remove a linha zero do eixo y
                            showticklabels=False
                        ), 
                        legend=dict(
                            font=dict(size=13),
                        )
    )
    return fig4

'''============================# Gráfico 5 #==================================='''
def metodo_de_pagamento(df, gender_filter):
    pagamentos = df['Método_de_pagamento']
    df_metodo_pagamento = pagamentos.value_counts().sort_values(ascending=False).reset_index(name='Quantidade')
    sort_df_metodo_pagamento = df_metodo_pagamento.sort_values(by='Quantidade')

    # Função para ajustar a posição do texto dinamicamente com base no gênero selecionado
    def ajustar_textposition(y_values, gender_filter):
        if gender_filter == 'All':
            return ["bottom center" if y < 130 else "bottom center" if y > 655 else "top center" for y in y_values]
        elif gender_filter == 'Masculino':
            return ["bottom center" if y > 460 else "top center" for y in y_values]
        elif gender_filter == 'Feminino':
            return ["bottom center" if y > 215 else "top center" for y in y_values]
        return ["top center" for _ in y_values]  # Padrão de fallback
    

    # Criar o gráfico de linhas
    fig = px.line(sort_df_metodo_pagamento, 
                x='Método_de_pagamento', 
                y='Quantidade', 
                text='Quantidade',   # Exibe os valores nos pontos
                markers=True,      # Adiciona marcadores nos pontos da linha
                
                )

    fig.update_traces(marker_color='blue',
                      marker = dict(size = 9),  
                      line=dict(color = 'blue', width=4), 
                      textposition=ajustar_textposition(sort_df_metodo_pagamento['Quantidade'], 
                                                        gender_filter)
                    ) 
    fig.update_layout(
        main_config, 
        height = 250, 
        xaxis=dict(
            title_text="",
            showgrid=False,  # Remove a linha de grade do eixo x
            zeroline=True,  # Remove a linha zero do eixo x
            showticklabels=True, 
            # tickangle=45
            
        ),
        yaxis=dict(
            title_text="",
            showgrid=True,  # Remove a linha de grade do eixo y
            zeroline=True,  # Remove a linha zero do eixo y
            showticklabels=False, 
            gridwidth=0.01, 
            gridcolor="gray", 
        ), 
           
    )

    return fig

'''============================# Gráfico 6 #==================================='''
def plot_demanda_clothing(df):
    # Definindo a ordem correta das estações
    ordem_temporadas = ['Verão', 'Outono', 'Inverno', 'Primavera']

    # Garantindo que a coluna 'Temporada' tenha a ordem correta
    df['Temporada'] = pd.Categorical(df['Temporada'], categories=ordem_temporadas, ordered=True)
    
    # Filtrar apenas a categoria "Clothing"
    clothing_df = df[df['Categoria'] == 'Roupas']
    
    # Contar os produtos mais populares em cada temporada
    demanda_clothing_por_temporada = (
        clothing_df.groupby(['Temporada', 'Categoria', 'Item_comprado'], observed=False)
        .size()
        .reset_index(name='Contagem'))
    
    # Encontrar o produto mais comprado em cada temporada
    produto_mais_demandado = demanda_clothing_por_temporada.loc[
        demanda_clothing_por_temporada.groupby('Temporada', observed=False)['Contagem'].idxmax()]
    
    # Ordenando explicitamente pela temporada
    # produto_mais_demandado = produto_mais_demandado.sort_values(by='Temporada')

    # Criar o gráfico de barras
    fig6 = px.bar(
        produto_mais_demandado, 
        x='Temporada', 
        y='Contagem', 
        text='Item_comprado',
        color='Item_comprado',
        labels={'Temporada': 'Estação', 'Item_comprado': 'Produto'}, 
        color_discrete_sequence=[px.colors.sequential.Cividis_r[8]]
    )
    
    # Ajustar a exibição do texto nas barras
    fig6.update_traces(texttemplate='%{text}', textposition='inside')
    fig6.update_layout(
        main_config,
        height=250,
        showlegend=False, 
        uniformtext_minsize=5, 
        uniformtext_mode='show', 
        font=dict(color='white', size=15),  # Texto em branco
        xaxis=dict(
            visible=True,
            title='Temporada',  
            showgrid=False,  # Remove a linha de grade do eixo x
            zeroline=True,  # Remove a linha zero do eixo x
            showticklabels=True, 
            tickangle=45, 
            showline=True, 
            linecolor='gray',  # Cor da linha
            linewidth=2,
        categoryorder='array',  # Força a ordenação pela lista definida
        categoryarray=ordem_temporadas  # Defina explicitamente a ordem das categorias
    ),
    yaxis=dict(
        visible=False,
        showgrid=False,  # Remove a linha de grade do eixo y
        zeroline=False,  # Remove a linha zero do eixo y
        showticklabels=False
        )
    )
    
    return fig6

'''============================# Gráfico 7 #==================================='''
def produtos_com_mais_receita(df):
    # agrupando dados
    receita_por_produto = df.groupby('Categoria')['Valor_da_compra_(USD)'].sum().reset_index().sort_values(by = 'Valor_da_compra_(USD)', ascending = False)

    # Seus dados
    color_discrete_sequence = [ 'gold', '#00224E', 'blue', '#2C6A8C' ]

    # Criando o gráfico de pizza
    fig = px.pie(receita_por_produto, 
                values='Valor_da_compra_(USD)', 
                names='Categoria', 
                hole = 0.4, 
                )

    # Atualizando o gráfico
    fig.update_traces(
        marker=dict(colors=color_discrete_sequence, line=dict(color='#303030', width=3)),
        hovertemplate="<b>%{label}</b><br>Valor: %{value}<br>Percentual: %{percent}",  
    )
    # Removendo a legenda
    fig.update_layout( 
                    main_config,
                    height=300, 
                    legend=dict(
                            orientation="h",  # Torna a legenda horizontal
                            y=-0.2            # Move a legenda para baixo
                    ), 
            
                )

    return fig


'''============================# CallBacks #==============================='''
@app.callback(
    Output("url", "pathname"), 
    Input("btn-page2", "n_clicks"),
    prevent_initial_call=True
)
def go_to_page2(n_clicks):
    return "/page2"


# callback que controla as paginas do dashboard
@app.callback(
    Output("dropdown-content", "is_open"),
    Input("toggle-dropdown", "n_clicks"),
    State("dropdown-content", "is_open")
)
def toggle_dropdown(n_clicks, is_open):
    if n_clicks:
        return not is_open  
    return is_open


#callback do filtro por genero
@app.callback(
    [Output("filter-dropdown-content", "is_open"),  
     Output('selected-filter', 'data')],  
    [
        Input("toggle-filter-dropdown", "n_clicks"), 
        Input("gender-all", "n_clicks"),  
        Input("gender-male", "n_clicks"),
        Input("gender-female", "n_clicks")
    ],
    State("filter-dropdown-content", "is_open")  #
)
def toggle_filter_dropdown(n, n_clicks_all, n_clicks_male, n_clicks_female, is_open):
    ctx = dash.callback_context

    # Verifica qual botão foi clicado
    if not ctx.triggered:
        return is_open, dash.no_update  # Mantém o estado atual do dropdown e não atualiza o filtro

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # Se qualquer botão de gênero for clicado, fecha o dropdown e atualiza o filtro
    if button_id in ["gender-all", "gender-male", "gender-female"]:
        return False, button_id  # Fecha o dropdown e armazena o filtro selecionado

    # Se o botão de toggle foi clicado, alterna o estado do dropdown
    if button_id == "toggle-filter-dropdown":
        return not is_open, dash.no_update  # Alterna entre abrir e fechar sem atualizar o filtro

    return is_open, dash.no_update  # Mantém o estado atual do dropdown e não altera o filtro


#callback que estiliza os botoes salvando a utima opção do usuario
@app.callback(
    [
        Output("gender-all", "style"),
        Output("gender-male", "style"),
        Output("gender-female", "style")
    ],
    [Input('selected-filter', 'data')]
)
def highlight_selected_filter(selected_filter):
    # Estilos padrão para os botões
    # dropdown-content", "is_open"),
    # toggle-dropdown", "n_clicks"),
    # dropdown-content", "is_open")
    default_style = {'background-color': '#17a2b8', 'color': 'white'}
    selected_style = {'background-color': '#0056b3', 'color': 'white'}  # Azul escuro para destaque

    # Definindo a cor do fundo dependendo do filtro selecionado
    style_all = selected_style if selected_filter == 'gender-all' else default_style
    style_male = selected_style if selected_filter == 'gender-male' else default_style
    style_female = selected_style if selected_filter == 'gender-female' else default_style
    # style_dropdown-content = selected_style if selected_filter == 'gender-female' else default_style


    return style_all, style_male, style_female


# callback dos graficos
@app.callback(
    [
        Output('graph_1', 'figure'),
        Output('graph_2', 'figure'),
        Output('graph_3', 'figure'),
        Output('graph_4', 'figure'),
        Output('graph_5', 'figure'), 
        Output('graph_6', 'figure'),
        Output('graph_7', 'figure'),
    ],
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

    # Criando gráficos
    graph_1 = distribuicao_idade(filtered_df)
    graph_2 = distribuicao_genero(filtered_df, gender_filter)
    graph_3 = compras_por_temporada(filtered_df)
    graph_4 = distribuicao_por_tamanho(filtered_df)
    graph_5 = metodo_de_pagamento(filtered_df, gender_filter)
    graph_6 = plot_demanda_clothing(filtered_df)
    graph_7 = produtos_com_mais_receita(filtered_df)

    return (
        graph_1,
        graph_2,
        graph_3,
        graph_4,
        graph_5, 
        graph_6, 
        graph_7
    )



@app.callback(
    Output("sidebar", "className"),
    [Input("sidebar-toggle", "n_clicks")],
    [State("sidebar", "className")],
)
def toggle_classname(n, classname):
    if n and classname == "":
        return "collapsed"
    return ""


@app.callback(
    Output("collapse", "is_open"),
    [Input("navbar-toggle", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


if __name__ == "__main__":
    # app.run_server(port=8588, debug=True)
    # app.run_server(host='0.0.0.0', debug = True, port=int(os.environ.get('PORT', 8588)))
    app.run_server(host='0.0.0.0', port=int(os.environ.get('PORT', 8050)))
