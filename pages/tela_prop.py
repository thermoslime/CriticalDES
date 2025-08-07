'''
Tela de propriedades
'''

# Importação das bibliotecas
from dash import html, dcc
import dash_bootstrap_components as dbc
import dash
from dados.Funcoes import Get_components

# Registro da página
dash.register_page(__name__,  path="/pages/tela_propriedade")


opcoes = Get_components()

##################### Layout da pagina ################
layout = dbc.Container([

    html.Div(children = [

        html.Div(id = "DES_Table"),

        # Itens
        dbc.Accordion([

            #Density
            dbc.AccordionItem(children = html.Div([
                    
                    html.P("It is possible to use the correlation developed by Haghbakhsh et al. (2019) for binary DES and with a temperature range from 283.15 K to 373.15 K. The equation to this model is:", style={'textAlign': 'left',  "fontSize": "1.5em"}),

                    dcc.Markdown(r'''
                $$
                    \begin{aligned}
                \rho (g/mL) =~ -1.13 \times 10^{-10} (T_{c,DES}^2) ~&+~ 2.566 \times 10^{-3} (T_{c, DES} ~+~ 0.2376 (\omega_{DES}^{0.2211}) ~-~ 
                \\ 4.67 \times 10^{-4} (V_{c, DES}) ~&-~ 4.64 \times 10^{-4} (T)\end{aligned}$$''',
                mathjax= True, style={"display": "flex", "justifyContent": "center", "fontSize": "1.2em"}),

                    html.Br(),

                    html.P("Another correlation was developed by Boublia et al. (2023) who obtained a model applicable to ternary DES, with a smaller deviation when compared to the Haghbakhsh correlation. It is given by:", style={'textAlign': 'left',  "fontSize": "1.5em"}),

                    dcc.Markdown(r'''
                $$
                    \begin{aligned}
                \rho (g/mL) ~=~ -&4.717 \times 10^{-7} (T_{c,DES}^2) ~+~ 9.098  \times 10^{-4} (T_{c, DES}) ~+~ 7.1965 \times 10^{-2} (\omega_{DES}^{0.67131}) ~-~ 2.034 \times 10^{-3} (V_{c, DES}) ~-~ \\ 
                &6.540 \times 10^{-4} (T) ~-~ 6.051 \times 10^{-5} (P_{c, DES}) ~+~ 6.1911 \times 10^{-3} (M_W) ~+~ 0.8597
                    \end{aligned}
                $$''', mathjax= True, style={"display": "flex", "justifyContent": "center", "fontSize": "1.2em", "paddingLeft": "100px"}),


                    html.Br(),

                    html.Div(id = "Density"),

                    html.Br(),

                ]), style={'width': '100%'}, title = html.H2('Density'), item_id = 'id0'),


            #Speeds of sound
            dbc.AccordionItem(children = html.Div([
                    
                    html.P("In 2020, Peyrovedin et al.  developed a model to estimate the speed of sound to use the correlation, using 420 experimental data covering 39 different DES. This correlation was obtained with most binary DES data. The equation to this model is:", style={'textAlign': 'left',  "fontSize": "1.5em"}),

                    dcc.Markdown(r'''
                $$
                    \begin{aligned}
                u (m/s) =~ \omega [7.378 M_W - 2.012 T] - 2.911 V_c + 2514.2
                     \end{aligned}
                $$''', mathjax= True, style={"display": "flex", "justifyContent": "center", "fontSize": "1.3em"}),

                    html.Div(id = "Speed"),

                    html.Br(),
                    html.Br(),

                ]), style={'width': '100%'}, title = html.H2('Speed of sound'), item_id = 'id1'),


            #Heat Capacity
            dbc.AccordionItem(children = html.Div([
                    
                    html.P("In 2020, Taherzadeh et al. developed a general correlation to calculate the heat capacity of DES, using 505 experimental data, in a temperature range from 278.15 to 363.15 K. This correlation was obtained with most binary DES data. The equation to this model is:", style={'textAlign': 'left',  "fontSize": "1.5em"}),

                    dcc.Markdown(r'''
                $$
                    \begin{aligned}
                C_p (J/mol.K) =~ {3.8 \times 10^{-4}} \frac{M_W ^ 3}{P_c ^6 } + {6.3 \times 10^{-5}} M_W ^ {2 \omega} + \frac{-24,577.4}{M_W} - 94.9 + 132.27 T ^ {1/4}
                     \end{aligned}
                $$''', mathjax= True, style={"display": "flex", "justifyContent": "center", "fontSize": "1.3em"}),

                    html.Div(id = "Heat"),

                    html.Br(),
                    html.Br(),

                ]), style={'width': '100%'}, title = html.H2('Heat capacity'), item_id = 'id2'),


            #Viscosity
            dbc.AccordionItem(children = html.Div([
                    
                    html.P("To organic compounds and conventional liquids, Lewis and Squides (1934) developed a global correlation to viscosity, where a reference data is necessary. The equation to this model is:", style={'textAlign': 'left',  "fontSize": "1.5em"}),

                    dcc.Markdown(r'''
                $$
                    \begin{aligned}
                \mu ^ {0.2661} (cP) ~=~ \mu_k ^ {-0.2661} + \frac {T - T_k} {233}
                     \end{aligned}
                $$''', mathjax= True, style={"display": "flex", "justifyContent": "center", "fontSize": "1.3em"}),

                    html.Br(),

                    html.P("In 2020 Bakhtyari A. et al. developed a general model to estimate the viscosity of binary DES, using 1308 experimental data, and 156 DES. It requires Pc, Tc and a reference date. It is given by:", style={'textAlign': 'left',  "fontSize": "1.5em"}),

                    dcc.Markdown(r'''
                $$
                    \begin{aligned}
                \mu (Pa . s) ~=~ \left[\mu_k ^ {\frac{-0.817}{P_c} - 0.123} - 1.595 T_c \left(\frac {T_k - T} {T ~~ T_k} \right) \right] ^ {\frac {1} {\frac{-0.817} {P_c} - 0.123}}
                    \end{aligned}
                $$''', mathjax= True, style={"display": "flex", "justifyContent": "center", "fontSize": "1.3em", "paddingLeft": "100px"}),


                    html.Br(),

                    ############### Input data ##################
                    dbc.Table([
                        html.Tbody([
                            html.Tr([html.Th('', style={'textAlign': 'center', 'width': '30%'}), html.Th('Value', style={'textAlign': 'center', 'width': '50%'}), html.Th('Unit', style={'textAlign': 'center', 'width': '20%'})]),

                            html.Tr([html.Td(html.P('Temperature Reference', style={'textAlign': 'left',  "fontSize": "1.2em"})),
                                    
                                    html.Td([
                                            dcc.Input(id='Ref_temperature', type='number',  value = 273.15, min = 273.15, max = 373.15, 
                                                    style={'textAlign': 'center', 'width': '100%'},
                                                    persistence = True,  placeholder="273.15 - 373.15", persistence_type = "session")
                                        ]),

                                    html.Td([
                                            dcc.Dropdown(id='TemperatureUnit_ref', options=['K'], value='K',
                                                        multi=False,
                                                        clearable=False,
                                                        disabled= False,
                                                        persistence = True, persistence_type = "session",
                                                        style={'textAlign': 'center', 'width': '100%'})
                                        ]),
                                        ]),

                            html.Tr([html.Td(html.P('Viscosity Reference', style={'textAlign': 'left',  "fontSize": "1.2em"})),
                                    
                                    html.Td([
                                            dcc.Input(id='Ref_viscosity', type='number',  value = 273.15, min = 0, 
                                                    style={'textAlign': 'center', 'width': '100%'},
                                                    persistence = True,  persistence_type = "session")
                                        ]),

                                    html.Td([
                                            dcc.Dropdown(id='viscosityUnit_ref', options=['Pa . s', 'mPa . s'], value='Pa . s',
                                                        multi=False,
                                                        clearable=False,
                                                        disabled= False,
                                                        persistence = True, persistence_type = "session",
                                                        style={'textAlign': 'center', 'width': '100%'})
                                        ]),
                                        ]),
                        
                        ])  # Final do Tbody
                    ], bordered=True),  # Final da tabela

                    html.Br(),
                    
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Viscosity estimation", id='viscosity_button', n_clicks=0, outline=True, color="primary", className="me-1 w-100"), 
                            dbc.Tooltip("Estimation of viscosity using reference values", target="viscosity_button")
                        ], width=6),
                        dbc.Col(
                            id = 'local_download_visco', width=6)]
                    ),
                    
                    html.Br(),
                    html.Br(),
                    
                    html.Div(id = "Viscosity"),

                    html.Br(),
                    html.Br(),

                ]), style={'width': '100%'}, title = html.H2('Viscosities'), item_id = 'id3'),



        
        ], always_open= True, flush = False, start_collapsed = False, active_item = ['id0', 'id1', 'id2', 'id3']),

        html.Br(),
        html.Br()

    ])
])

