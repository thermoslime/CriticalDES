'''
Tela de dados da aplicação
'''

# Importação das bibliotecas
from dash import html, dcc
import dash_bootstrap_components as dbc
import dash
from dados.Funcoes import Get_components

# Registro da página
dash.register_page(__name__,  path="/pages/tela_critical")


opcoes = Get_components()

##################### Layout da pagina ################
layout = dbc.Container([

    html.Div(children = [
        html.Br(),
        html.P('''Enter with the DES composition:''', style={'textAlign': 'left',  "fontSize": "1.5em"}),
        html.Br()
    ]),


    ################## parâmetros ##########################

    # Div com as informações interativas
    html.Div(id="dados_interativos", children=[
        
        html.Div([
            # Tabela com os nomes
            dbc.Table([
                html.Tbody([
                    # primeira linha - titulos
                    html.Tr([html.Th(''), 
                             html.Th('Names', style={'textAlign': 'center', 'width': '60%'}), 
                             html.Th( dcc.Dropdown(id='FracUnit', options=[{'label': 'Mole fraction (Xi)', 'value' : 'Xi'},
                                                                           {'label': 'Molar proportion (:)', 'value' : 'ni'}], value='Xi',
                                                multi=False,
                                                clearable=False,
                                                disabled= False,
                                                persistence = True, persistence_type = "session",
                                                style={'textAlign': 'center', 'width': '100%'}), style={'textAlign': 'center', 'width': '20%'})]
                             ),

                    # segunda linha
                    html.Tr([
                        html.Td(html.P('Component 1', style={'width': '100%', 'textAlign': 'left',  "fontSize": "1.2em"})),
                        
                        html.Td([
                            dcc.Dropdown(id='Nome_1', options= opcoes, value= opcoes[1], 
                                         multi=False, clearable=False, disabled= False, persistence = True, 
                                         persistence_type = "session", style={'width': '100%', 'textAlign': 'center'})
                                ]),

                        html.Td([dcc.Input(id='frac_1', type='number', min = 0, value = 0.5, step = 'any',
                                            style={'width': '100%', 'textAlign': 'center'},
                                            persistence = True, persistence_type = 'session')
                                ]),
                                ]),
                    
                    # terceira linha
                    html.Tr([
                        html.Td(html.P('Component 2', style={'textAlign': 'left',  "fontSize": "1.2em"})),
                            
                        html.Td([
                            dcc.Dropdown(id='Nome_2', options= opcoes, value= opcoes[2],
                                         multi=False, clearable=False, disabled= False, persistence = True, 
                                         persistence_type = "session", style={'width': '100%', 'textAlign': 'center'})
                                ]),
                        html.Td([dcc.Input(id='frac_2', type='number', min = 0, value = 0.5, step = 'any',
                                            style={'width': '100%', 'textAlign': 'center'}, 
                                            persistence = True, persistence_type = 'session')
                                ]),
                            ]),
                    
                    # quarta linha
                    html.Tr([
                        html.Td(html.P('Component 3', style={'textAlign': 'left',  "fontSize": "1.2em"})),
                        html.Td([
                            dcc.Dropdown(id='Nome_3', options= opcoes, value= opcoes[0], 
                                         multi=False, clearable=False, disabled= False, persistence = True, 
                                         persistence_type = "session", style={'width': '100%', 'textAlign': 'center'})
                                ]),
                        html.Td([
                            dcc.Input(id='frac_3', type='number', min = 0, value = 0, step = 'any',
                                      style={'width': '100%', 'textAlign': 'center'}, disabled = False,
                                      persistence = True, persistence_type = 'session')
                                ]),
                            ]),
                ])  # Final do Tbody
            ], bordered=True),  # Final da tabela

        ]),  # Final do Div dos parametros


    # Inicio dos cálculos
    html.Br(),
    dbc.Button("Critical Properties", id='critical_button', n_clicks=0, outline=True, color="primary", className="me-1 w-100"),
    dbc.Tooltip("Calculate the critical properties of the system", target="critical_button"),

    html.Br(),
    html.Br(),

    # Componente de carregamento
    dcc.Loading(
        id = "Icone_Loading",
        type="circle",  # Tipo de ícone (pode ser "circle", "dot", ou "default")
        children = html.Div(id = "Tabela")  # O que vai ser mostrado no final
    ),

    html.Br(),
    html.Br()
    
    ])
])
