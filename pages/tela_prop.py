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
        html.Br(),
        
        html.H1("Density"),
        
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
    &6.540 \times 10^{-4} (T) ~-~ 6.051 \times 10^{-5} (P_{c, DES}) ~+~ 6.1911 \times 10^{-3} (M_{DES}) ~+~ 0.8597
        \end{aligned}
    $$''', mathjax= True, style={"display": "flex", "justifyContent": "center", "fontSize": "1.2em", "paddingLeft": "100px"}),


        html.Br(),

        html.Div(id = "Propriedade"),

        html.Br(),
        html.Br() 
    ]),

])

