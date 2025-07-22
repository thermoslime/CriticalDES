'''
Tela Inicial da aplicação
'''

# Importação das bibliotecas
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import dash

# Registro da página
dash.register_page( __name__, path="/", name = "Tela Inicial")

# Criando variáveis para cada seção do conteúdo


# Introdução
layout  = html.Div(id="intro", children=[
    html.H1("About"),

    html.P('''This web application was developed to estimate critical properties of binary and ternary deep eutectic solvents (DES) using a group contribution method with the Lee–Kesler mixing rule. Additionally, the app allows users to calculate density using two empirical equations.''', style={'text-align': 'justify', "fontSize": "1.5em"}),

    html.P([
            
        '''This work is based on the paper by Boublia A. et. el. (2023), which provides a user-friendly Excel worksheet. The publication is available at: : ''', 

            
            html.A("Critical Properties of Ternary Deep Eutectic Solvents Using Group Contribution with Extended Lee−Kesler Mixing Rules.", href="https://pubs.acs.org/doi/10.1021/acsomega.3c00436", target="_blank"),
    ], style={'text-align': 'justify', "fontSize": "1.5em"}
           ),

    html.P('''This application was developed by LTS (Laboratório de Termodinâmica e Processos de Separação), at UFC – Universidade Federal do Ceará, Brazil. For contact, please email:: modelosdegibbs@gmail.com.''', style={'text-align': 'justify', "fontSize": "1.5em"}),

    html.Br(),

    html.H1("Equations"),

    html.P('''The equations used are presented below, and were used by Boublia A. et. el. (2023) to estimate the the molecular weight (M), boiling temperature (Tb), critical volume (Vc), critical temperature (Tc), critical pressure (Pc) and acentric factor (ω).''', style={'text-align': 'justify', "fontSize": "1.5em"}),




   html.P(
         [html.B('Modified Lydersen−Joback−Reid group contribution method: '),
           ' Used to calculate the critical properties of components used structural groups.'],
         style={'text-align': 'justify', "fontSize": "1.5em"}),   
    
    dcc.Markdown(r'''
    $$M (g/mol) ~=~ \sum {z_i \Delta M_i}$$
    ''', mathjax= True, style={'text-align': 'justify', "fontSize": "1.5em", "paddingLeft": "100px"}),

    dcc.Markdown(r'''
    $$T_b (K) ~=~ 198.2 ~+~ \sum {z_i \Delta T_{b Mi}}$$
    ''', mathjax= True, style={'text-align': 'justify', "fontSize": "1.5em", "paddingLeft": "100px"}),

    dcc.Markdown(r'''
    $$V_c (mL/mol) ~=~ 6.75 ~+~ \sum {z_i \Delta V_{c Mi}}$$
    ''', mathjax= True, style={'text-align': 'justify', "fontSize": "1.5em", "paddingLeft": "100px"}),

    dcc.Markdown(r'''
    $$T_c (K) ~=~ \frac {T_b}{0.5703 ~+~ 1.0121 ~\sum {z_i \Delta T_{cMi}} ~-~ (\sum {z_i \Delta T_{c Mi}})^2}$$
    ''', mathjax= True, style={'text-align': 'justify', "fontSize": "1.5em", "paddingLeft": "100px"}),


    dcc.Markdown(r'''
    $$P_c (bar) ~=~ \frac{M}{(0.2573 ~+~ \sum {z_i \Delta P_{cMi}})^2}$$
    ''', mathjax= True, style={'text-align': 'justify', "fontSize": "1.5em", "paddingLeft": "100px"}),

    dcc.Markdown(r'''
    $$\omega ~=~ \frac{(T_b ~-~ 43) (T_c ~-~ 43)}{(T_c ~-~ T_b) (0.7 T_c ~-~ 43)} \log_{10}(\frac{P_c}{1.101325}) ~-~ \frac{(T_c ~-~ 43)}{(T_c ~-~ T_b)} \log_{10}(\frac{P_c}{1.101325}) ~+~ \log_{10}(\frac{P_c}{1.01325}) ~-~ 1$$
    ''', mathjax= True, style={'text-align': 'justify', "fontSize": "1.5em", "paddingLeft": "100px"}),


    # EQUATIONS MIXING RULES
     html.P(
         [html.B('Extended Lee-Kesler Mixing Rules: '),
           ' Used to calculate the critical properties of DES.'],
         style={'text-align': 'justify', "fontSize": "1.5em"}),   
    
    dcc.Markdown(r'''
    $$M_{DES} (g/mol) ~=~ \sum_{n=1}^{3} {x_n M_n}$$
    ''', mathjax= True, style={'text-align': 'justify', "fontSize": "1.5em", "paddingLeft": "100px"}),

    dcc.Markdown(r'''
    $$V_{c, DES} (mL/mol) ~=~ \sum_{n=1}^{3} { \sum_{m=1}^{3} {x_n  x_m  V_{c, nm}} }$$
    ''', mathjax= True, style={'text-align': 'justify', "fontSize": "1.5em", "paddingLeft": "100px"}),

    dcc.Markdown(r'''
    $$T_{c, DES} (K) ~=~ \frac{1}{V_{c, DES}^{0.25}} ~  \sum_{n=1}^{3} { \sum_{m=1}^{3} {x_n  x_m  V_{c, nm}^{0.25} ~ T_{c, nm}} }$$
    ''', mathjax= True, style={'text-align': 'justify', "fontSize": "1.5em", "paddingLeft": "100px"}),

    dcc.Markdown(r'''
    $$P_{c, DES} (bar) ~=~ (0.2905 - 0.0850 ~ \omega_{DES})\frac{83.1447 T_{c, DES}}{V_{c, DES}}$$
    ''', mathjax= True, style={'text-align': 'justify', "fontSize": "1.5em", "paddingLeft": "100px"}),

    dcc.Markdown(r'''
    $$\omega_{DES} ~=~ \sum_{n=1}^{3} {x_n \omega_n}$$
    ''', mathjax= True, style={'text-align': 'justify', "fontSize": "1.5em", "paddingLeft": "100px"}),

    dcc.Markdown(r'''
    $$V_{c, nm} (mL/mol) ~=~ \frac{1}{8} ~ ({V_{c,n}^{1/3}} + {V_{c,m}^{1/3}})^3$$
    ''', mathjax= True, style={'text-align': 'justify', "fontSize": "1.5em", "paddingLeft": "100px"}),

    dcc.Markdown(r'''
    $$T_{c, nm} (K) ~=~  (T_{c,n} ~ T_{c,m})^{0.5}$$
    ''', mathjax= True, style={'text-align': 'justify', "fontSize": "1.5em", "paddingLeft": "100px"}),


    html.Br(),

    html.H1("References"),
        html.Ul([
        html.Li("ABDOLLAHZADEH, Mohammadjavad et al. Estimating the density of deep eutectic solvents applying supervised machine learning techniques. Scientific Reports 2022 12:1, v. 12, n. 1, p. 1–16, 23 mar. 2022.;"),
        html.Li("BOUBLIA, Abir et al. Critical Properties of Ternary Deep Eutectic Solvents Using Group Contribution with Extended Lee-Kesler Mixing Rules. ACS Omega, v. 8, n. 14, p. 13177–13191, 11 abr. 2023;"),
        html.Li("HAGHBAKHSH, Reza et al. Simple and global correlation for the densities of deep eutectic solvents. Journal of Molecular Liquids, v. 296, p. 111830, 15 dez. 2019.;"),
        html.Li("OMAR, Karzan A.; SADEGHI, Rahmat. Database of deep eutectic solvents and their physical properties: A review. Journal of Molecular Liquids, v. 384, p. 121899, 15 ago. 2023. ;"),
        html.Li("VALDERRAMA, José O.; FORERO, Luis A.; ROJAS, Roberto E. Critical properties and normal boiling temperature of ionic liquids. Update and a new consistency test. Industrial and Engineering Chemistry Research, v. 51, n. 22, p. 7838–7844, 6 jun. 2012;"),
    ], style={'text-align': 'justify', "fontSize": "1.2em"}),

    html.Br(),
    html.Br()




], style={"padding-top": "10px"})
