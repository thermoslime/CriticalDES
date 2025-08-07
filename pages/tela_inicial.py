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
    
    ################# ABOUT ######################
    html.H1("About"),

    html.P('''This web application was developed to estimate critical properties of binary and ternary deep eutectic solvents (DES) using a group contribution method with the Lee–Kesler mixing rule. Additionally, this application allows the estimation of some properties using correlations present in the literature.''', style={'text-align': 'justify', "fontSize": "1.5em"}),

    html.P([
        '''This work is based on the paper by Boublia A. et el. (2023), which provides a user-friendly Excel worksheet. The publication is available at: : ''', 

            html.A("Critical Properties of Ternary Deep Eutectic Solvents Using Group Contribution with Extended Lee−Kesler Mixing Rules.", href="https://pubs.acs.org/doi/10.1021/acsomega.3c00436", target="_blank"),
    ], style={'text-align': 'justify', "fontSize": "1.5em"}
           ),

    html.P([
          '''This application was developed by Quinto F. H. B. of the Laboratory of Thermodynamics and Separation Processes (LTS) of the Federal University of Ceará, Brazil. Contact email: ''', 
          html.Strong("lts@ufc.br", style = {"color": "blue"})], 
        style={'text-align': 'justify', "fontSize": "1.5em"}),

    html.Br(),

    ################# EQUATION ######################
    html.H1("Equations"),

    html.P('''The equations presented below, for the calculation of critical properties, are widely used in the literature for binary DES systems, and were applied by Boublia A. et el. (2023) for ternaries, obtaining coherent results and good fits to the experimental data. The properties obtained are: the molecular weight (M), boiling temperature (Tb), critical volume (Vc), critical temperature (Tc), critical pressure (Pc) and acentric factor (ω).''', style={'text-align': 'justify', "fontSize": "1.5em"}),

    html.P('''Click on the sections below to expand or collapse the content with the implemented formulas of this application.''', style={'text-align': 'justify', "fontSize": "1.5em"}),
    dbc.Accordion([
        
        dbc.AccordionItem(children = html.Div([
            html.P(['Method used to estimate the critical properties of components from defined structural groups. It was proposed by Alvarez and Valderrama (2004), who combined the best results from two correlations, obtaining good results for high molecular weight molecules.'],
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

              
              html.P(['Where: '],
                  style={'text-align': 'justify', "fontSize": "1.5em"}),   

              dcc.Markdown(r'''
              - $z_i$: Number of occurrences of group i  
              - $\Delta M_i$: Molecular mass of group i  
              - $\Delta T_{bMi}$: Boiling temperature contribution of group i
              - $\Delta V_{cMi}$: Critical volume contribution of group i
              - $\Delta T_{cMi}$: Critical temperature contribution of group i
              - $\Delta P_{cMi}$: Critical pressure contribution of group i
              ''', mathjax= True, style={'text-align': 'justify', "fontSize": "1.5em", "paddingLeft": "100px"}),

              html.Br(),
              html.Br(),

        ]), style={'width': '100%'}, title = html.B('Modified Lydersen−Joback−Reid group contribution method',  style={'text-align': 'justify', "fontSize": "1.5em"}), item_id = 'id0'),


        dbc.AccordionItem(children = html.Div([
            html.P('After obtaining the critical properties of the components, the mixing rule is used to obtain the properties of the binary DES. The equations were modified for the cases of ternary DES, as explained by Boublia A. et al. (2023).',
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

              
              html.P(['Where: '],
                  style={'text-align': 'justify', "fontSize": "1.5em"}),   

              dcc.Markdown(r'''
              - $x_n$: Mole fraction mole of component n
              - $T_{c, nm}$: Binary Interation term  
              - $V_{c, nm}$: Binary Interation term
              ''', mathjax= True, style={'text-align': 'justify', "fontSize": "1.5em", "paddingLeft": "100px"}),

            html.Br(),
        ]), style={'width': '100%'}, title = html.B('Extended Lee-Kesler Mixing Rules',  style={'text-align': 'justify', "fontSize": "1.5em"}), item_id = 'id1')
    
    # End accordion
    ], always_open= True, flush = True, start_collapsed = True),


    html.Br(),

    ################# EQUATION ######################
    html.H1("References"),
      html.Ul([
          html.Li(r"Alvarez, V. H.; Valderrama, J. O. A modified Lydersen-Joback-Reid method to estimate the critical properties of biomolecules. Alimentaria. 2004, 254,55-66"),
          html.Li(r"Bakhtyari, A., Haghbakhsh, R., Duarte, A. R. C., & Raeissi, S. (2020). A simple model for the viscosities of deep eutectic solvents. Fluid Phase Equilibria, 521, 112662."),
          html.Li(r"Boublia, A., Lemaoui, T., Almustafa, G., Darwish, A. S., Benguerba, Y., Banat, F., & AlNashef, I. M. (2023). Critical Properties of Ternary Deep Eutectic Solvents Using Group Contribution with Extended Lee-Kesler Mixing Rules. ACS Omega, 8(14), 13177–13191."),
          html.Li(r"Haghbakhsh, R., Bardool, R., Bakhtyari, A., Duarte, A. R. C., & Raeissi, S. (2019). Simple and global correlation for the densities of deep eutectic solvents. Journal of Molecular Liquids, 296, 111830."),
          html.Li(r"Haghbakhsh, R., Taherzadeh, M., Duarte, A. R. C., & Raeissi, S. (2020). A general model for the surface tensions of deep eutectic solvents. Journal of Molecular Liquids, 307, 112972."),
          html.Li(r"Peyrovedin, H., Haghbakhsh, R., Duarte, A. R. C., & Raeissi, S. (2020). A Global Model for the Estimation of Speeds of Sound in Deep Eutectic Solvents. Molecules 2020, Vol. 25, Page 1626, 25(7), 1626."),
          html.Li(r"Taherzadeh, M., Haghbakhsh, R., Duarte, A. R. C., & Raeissi, S. (2020a). Estimation of the heat capacities of deep eutectic solvents. Journal of Molecular Liquids, 307, 112940."),
          html.Li(r"Taherzadeh, M., Haghbakhsh, R., Duarte, A. R. C., & Raeissi, S. (2020b). Generalized Model to Estimate the Refractive Indices of Deep Eutectic Solvents. Journal of Chemical and Engineering Data, 65(8), 3965–3976."),
          html.Li(r"Valderrama, J. O., Forero, L. A., & Rojas, R. E. (2012). Critical properties and normal boiling temperature of ionic liquids. Update and a new consistency test. Industrial and Engineering Chemistry Research, 51(22), 7838–7844."),
          html.Li(r"Valderrama, J. O., Forero, L. A., & Rojas, R. E. (2019). Critical Properties of Metal-Containing Ionic Liquids. Industrial and Engineering Chemistry Research, 58(17), 7332–7340."),
          html.Li(r"Valderrama, J. O., & Robles, P. A. (2007). Critical properties, normal boiling temperatures, and acentric factors of fifty ionic liquids. Industrial and Engineering Chemistry Research, 46(4), 1338–1344."),
          html.Li(r"Valderrama, J. O., Sanga, W. W., & Lazzús, J. A. (2008). Critical properties, normal boiling temperature, and acentric factor of another 200 ionic liquids. Industrial and Engineering Chemistry Research, 47(4), 1318–1330."),
], style={'text-align': 'justify', "fontSize": "1.2em"}),

    html.Br(),
    html.Br()




], style={"padding-top": "10px"})
