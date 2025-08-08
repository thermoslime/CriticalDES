# Importando as bibliotecas
from dash import Dash, html, dcc, State, dash_table, ctx
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash

# Importa a função que calcula as propriedades do DES
from dados.Funcoes import PropriedadesDes, Get_components, Density_Boublia, Density_Haghbakhsh, Speed_Peyrovedin, Cp_Mehrdad, viscosity_LewisSquires, viscosity_Bakhtyary, Grafico_viscosidade, df_references

# Usado na manipulação de matrizes
import numpy as np

# Usada para fazer download do csv
import pandas as pd

# Biblioteca para plotar gráficos interativos
import plotly.express as px
import plotly.graph_objects as go

# Usada em alguns Callbacks
from dash.exceptions import PreventUpdate


########### VARIÁVEIS ####################
colors = {
    'fundo': "#FFFFFF",
    'texto': "#0565E2",
    'destaque': '#FF6961',
    'botao': '#0F00FF',
}

# Constante dos gases ideais
R = 8.314 #J/molK

# Preparando os eixos das composições para os gráficos 2d
eixo_x = np.linspace(0, 1, 200)

# Preparando a lista com as composição x1 e x2. [[x1, x2], [x1, x2], ...]
eixo_xy = []

# Para cada composição x1, calculamos um x2 e adicionamos na lista "eixo_xy"
for i in eixo_x:
  eixo_xy.append([i, 1-i])

# Transformamos a lista em um array
eixo_xy = np.array(eixo_xy)


# Gráfico vazio, usado para quando não termos nenhum dado
grafico_vazio =  {'data': [], 'layout': {
    'xaxis': {'title': 'Eixo X'},
    'yaxis': {'title': 'Eixo Y'},
    'title': 'Clique no botão para gerar o gráfico'
}}

############################################

# Inicializando o aplicativo
app = Dash(__name__, external_stylesheets= [dbc.themes.BOOTSTRAP], suppress_callback_exceptions = True, use_pages=True)
server = app.server


############ principal ################

# Layout principal
app.layout = dbc.Container([

   dcc.Location(id='url', refresh=False),
   
   dbc.Navbar(
      dbc.Container([
        html.Div([
            html.Div("Critical properties to Deep Eutectic Solvents (DES)", className="fs-2 fw-bold text-white"),
            html.Div("Using modified Lydersen-Joback-Reid with Lee-Kesler mixing rule", className="fs-3 text-white-50"),
        ]),
        
        dbc.Nav([
               dcc.Link("Home", id = "Link_inicial",href = "/", className="btn btn-outline-light btn-lg  mx-2"),
               dbc.Tooltip("Inicial page", target="Link_inicial"),

               dcc.Link("Critical", id = "Link_critical", href="/pages/tela_critical", className="btn btn-outline-light btn-lg mx-2"),
               dbc.Tooltip("Get critical properties DES", target="Link_critical"),
            ], className="ms-auto d-flex")
    ]),

    color="primary",
    dark=True,
    sticky="top"
    ),

    # Linha de Links
    html.Div([
       # Local onde as páginas serão mostradas
       dash.page_container
    ], style={"paddingLeft": "30px", "paddingRight": "30px"}),
    
    
    dcc.Store(id = 'critical_des',  storage_type = 'session'),
    dcc.Store(id = 'critical_componentes',  storage_type = 'session'),
    
    dcc.Store(id = 'status', storage_type = 'session'),
    dcc.Store(id = 'url_page', storage_type = 'session'),

    dcc.Store(id = 'Density_Haghbakhsh', storage_type = 'session'),
    dcc.Store(id = 'Density_Boublia', storage_type = 'session'),

    dcc.Store(id = 'Speed_Peyrovedin', storage_type = 'session'),
    dcc.Store(id = 'Cp_Mehrdad', storage_type = 'session'),

    dcc.Store(id = 'fracoes_molares', storage_type = 'session'),

    dcc.Store(id = 'density_dados',  storage_type = 'session'),
    dcc.Store(id = 'viscosity_dados',  storage_type = 'session'),
    dcc.Store(id = 'cp_dados',  storage_type = 'session'),
    dcc.Store(id = 'speed_dados',  storage_type = 'session'),
],fluid=True)


##################### INTERATIVO #####################
# Armazenamento das frac
@app.callback(
    # Recebendo os valores na tela
    Output(component_id='url_page', component_property='data'),

    Input(component_id='url', component_property='pathname'),
)
def url_pag(pag):
   if pag == '/':
      return 'home'
   elif pag == '/pages/tela_critical':
      return 'data'
   else:
      return 'prop'


# Edição se ternário
@app.callback(
    # Recebendo os valores na tela
    Output(component_id='fracoes_molares', component_property='data'),

    Input(component_id='FracUnit', component_property='value'),
    
    Input(component_id='frac_1', component_property='value'),
    Input(component_id='frac_2', component_property='value'),
    Input(component_id='frac_3', component_property='value'),
)
def save_frac(escolha, v1, v2, v3):

   if escolha == 'Xi':
      x1 = v1
      x2 = v2
      x3 = v3

      return [x1, x2, x3]
   
   elif escolha != 'Xi':
      try:
         soma = v1 + v2 + v3
         x1 = v1 / soma
         x2 = v2 / soma
         x3 = v3 / soma

         return [x1, x2, x3]
      except:
         return [0, 0, 0]
   
   else:
      return [0, 0, 0]

   

# Edição se ternário
@app.callback(
    # Recebendo os valores na tela
    Output(component_id='frac_1', component_property='disabled'),
    Output(component_id='frac_2', component_property='disabled'),
    Output(component_id='frac_3', component_property='disabled'),

    Output(component_id='frac_1', component_property='value'),
    Output(component_id='frac_2', component_property='value'),
    Output(component_id='frac_3', component_property='value'),

    Input(component_id='Nome_1', component_property='value'),
    Input(component_id='Nome_2', component_property='value'),
    Input(component_id='Nome_3', component_property='value'),

    State(component_id='fracoes_molares', component_property='data'),
)
def sets_inalterar(name1, name2, name3, list_frac):
   
   nomes = [name1, name2, name3]

   if list_frac == None:
      valores = [0.5, 0.5, 0]
   
   else:
      valores = list_frac

   estados = [False] * 3

   for indice, valor in enumerate(nomes):
      if nomes[indice] == '/':
         estados[indice] = True
         valores[indice] = 0
      else:
         pass

   return estados[0], estados[1], estados[2], valores[0], valores[1], valores[2]


# Edição link
@app.callback(
    # Recebendo os valores na tela
    Output(component_id='Link_correlation', component_property= 'style'),
    Output(component_id='Link_correlation', component_property= 'className'),

   Input(component_id='critical_des', component_property='data'),
   Input(component_id='critical_componentes', component_property='data'),

)
def links_dinamic(des_tabel, comp_tabel):
   #className="btn btn-outline-light btn-lg"

   # Se existir algo
   if des_tabel != 'Error Type' and des_tabel != 'Error Sum' and des_tabel != None:

      df_des = pd.DataFrame(des_tabel)
      df_comp = pd.DataFrame(comp_tabel)

      try:
         count_nulo = df_comp['Abr.'].value_counts()['/']
      except:
         count_nulo = 0

      # Se houver 2 ou 3 componentes:
      if count_nulo <= 1:
         estilo = {'pointer-events': 'auto'}
         classe = "btn btn-outline-dark btn-lg mx-2"

         return estilo, classe
      
      else:
         estilo = {"pointerEvents": "auto", "cursor": "not-allowed", 'color': 'gray', "opacity": "0.85"}
         classe = "btn btn-outline-secondary btn-lg disabled mx-2"

         return estilo, classe
   
   else:
      estilo = {"pointerEvents": "auto", "cursor": "not-allowed", 'color': 'gray', "opacity": "0.85"}
      classe = "btn btn-outline-secondary btn-lg disabled mx-2"

      return estilo, classe



################ PROPRIEDADES ##############
# Mostrar as densidades, velocidade do som e Cp
@app.callback(
   # MENSAGENS NA TELA
   Output(component_id='DES_Tabela', component_property='children'),
   Output(component_id='Density', component_property='children'),
   Output(component_id='Speed', component_property='children'),
   Output(component_id='Heat', component_property='children'),

   # INPUTS
   Input(component_id='density_dados', component_property='data'),
   State(component_id= 'speed_dados',  component_property='data'),
   State(component_id= 'cp_dados',  component_property='data'),

   Input(component_id='critical_des', component_property='data'),
   Input(component_id='status', component_property='data'),
)
def prop_lab_label(dict_densidade, dict_speed, dict_cp, des_tabel, status):

   # Se existir algo
   if status != 'Error Type' and status != 'Error Sum' and status != None:

      df_densidade = pd.DataFrame(dict_densidade)
      df_speed = pd.DataFrame(dict_speed)
      df_cp = pd.DataFrame(dict_cp)
   

      tabela_des = html.Div([
         html.Br(),

         html.P(children = f'The properties below were obtained for DES:', style={'textAlign': 'left', "fontSize": "1.5em"}),

         dash_table.DataTable(
            data = round(pd.DataFrame(des_tabel), 4).to_dict('records'), #List of dict
            columns = [
               {"name": i, 
                "id": i, 
               } for i in pd.DataFrame(des_tabel).columns],
            
            style_cell={
               'fontSize': '18px',
               'textAlign': 'center',      # alinhamento horizontal
               'color': 'black',           # cor da fonte
            'backgroundColor': 'white', # cor do fundo da célula
            },

            style_header={
               'fontWeight': 'bold',
               'backgroundColor': "#abfcff",
               'fontSize': '20px',
               'color': 'black',
            }
         ),

         html.Br(),
         
         ])


      conteudo_densi = html.Div([ 
         html.Br(),
         html.P(children = 'The following values were obtained:', style={'textAlign': 'left', "fontSize": "1.5em"}),

         dash_table.DataTable(
            data = round(df_densidade, 4).to_dict('records'), #List of dict
            columns = [
               {"name": i, 
                  "id": i, 
               } for i in df_densidade.columns],

            style_table={
            'maxHeight': '300px',   # Altura máxima visível
            'overflowY': 'auto',    # Scroll vertical quando passar do limite
            'overflowX': 'auto',    # Scroll horizontal se precisar
         },
            
            style_cell={
               'fontSize': '18px',
               'textAlign': 'center',      # alinhamento horizontal
               'color': 'black',           # cor da fonte
               'backgroundColor': 'white', # cor do fundo da célula
               'minWidth': '100px',    # opcional para ajustar colunas
               'width': '100px',
               'maxWidth': '150px',
            },

            style_header={
               'fontWeight': 'bold',
               'backgroundColor': "#abfcff",
               'fontSize': '20px',
               'color': 'black',
            },
         ),

   ])
      
      conteudo_speed = html.Div([ 
         html.Br(),
         html.P(children = 'The following values were obtained:', style={'textAlign': 'left', "fontSize": "1.5em"}),

         dash_table.DataTable(
            data = round(df_speed, 4).to_dict('records'), #List of dict
            columns = [
               {"name": i, 
                  "id": i, 
               } for i in df_speed.columns],

            style_table={
            'maxHeight': '300px',   # Altura máxima visível
            'overflowY': 'auto',    # Scroll vertical quando passar do limite
            'overflowX': 'auto',    # Scroll horizontal se precisar
         },
            
            style_cell={
               'fontSize': '18px',
               'textAlign': 'center',      # alinhamento horizontal
               'color': 'black',           # cor da fonte
               'backgroundColor': 'white', # cor do fundo da célula
               'minWidth': '100px',    # opcional para ajustar colunas
               'width': '100px',
               'maxWidth': '150px',
            },

            style_header={
               'fontWeight': 'bold',
               'backgroundColor': "#abfcff",
               'fontSize': '20px',
               'color': 'black',
            },
         ),


      ])

      conteudo_cp = html.Div([ 
         html.Br(),
         html.P(children = 'The following values were obtained:', style={'textAlign': 'left', "fontSize": "1.5em"}),

         dash_table.DataTable(
            data = round(df_cp, 4).to_dict('records'), #List of dict
            columns = [
               {"name": i, 
                  "id": i, 
               } for i in df_cp.columns],

            style_table={
            'maxHeight': '300px',   # Altura máxima visível
            'overflowY': 'auto',    # Scroll vertical quando passar do limite
            'overflowX': 'auto',    # Scroll horizontal se precisar
         },
            
            style_cell={
               'fontSize': '18px',
               'textAlign': 'center',      # alinhamento horizontal
               'color': 'black',           # cor da fonte
               'backgroundColor': 'white', # cor do fundo da célula
               'minWidth': '100px',    # opcional para ajustar colunas
               'width': '100px',
               'maxWidth': '150px',
            },

            style_header={
               'fontWeight': 'bold',
               'backgroundColor': "#abfcff",
               'fontSize': '20px',
               'color': 'black',
            },
         ),

      ])


      
      return tabela_des, conteudo_densi, conteudo_speed, conteudo_cp
   
   else:
        mensagem = html.P(children = 'The chosen solvent is not a binary or ternary DES!', style={'color': 'red',
                                                                                                       'fontWeight': 'bold',
                                                                                                       'textAlign': 'left',  
                                                                                                       "fontSize": "1.2em"})

        return None, mensagem, mensagem, mensagem


@app.callback(
   # VALORES ARMAZENADOS
   Output(component_id= 'density_dados',  component_property='data'),
   Output(component_id= 'speed_dados',  component_property='data'),
   Output(component_id= 'cp_dados',  component_property='data'),

   # INPUTS
   Input(component_id='critical_des', component_property='data'),
   Input(component_id='status', component_property='data'),

)
def prop_lab_values(des_tabel, status):
   #className="btn btn-outline-light btn-lg"
   # Se existir algo
   if status != 'Error Type' and status != 'Error Sum' and status != None:
      eixo_temperature = np.arange(283.15, 374.15)
      df_des = pd.DataFrame(des_tabel)

      #################### CALCULO ###############
      
      # Propriedades para calcular a densidade
      Mw = df_des['Mw (g/mol)'][0]
      Vc = df_des['Vc (mL/mol)'][0]
      Tc = df_des['Tc (K)'][0]
      Pc = df_des['Pc (bar)'][0]
      w =  df_des['ω'][0]

      eixo_densi_haghbakhsh = []
      eixo_densi_boublia = []
      eixo_speed = []
      eixo_cp = []


      for temperature in eixo_temperature:
         densi_Haghbakhsh = Density_Haghbakhsh(temperature, Tc, Vc, w)
         densi_Boublia = Density_Boublia(temperature, Mw, Tc, Vc, Pc, w)

         speed = Speed_Peyrovedin(temperature, Mw, Vc, w)
         cp = Cp_Mehrdad(temperature, Mw, Pc, w)

         eixo_densi_haghbakhsh.append(densi_Haghbakhsh)
         eixo_densi_boublia.append(densi_Boublia)
         eixo_speed.append(speed)
         eixo_cp.append(cp)
      

      df_densidade = pd.DataFrame({
         "Temperature (K)" : eixo_temperature,
         "Haghbakhsh correlation (g/cm3)" : eixo_densi_haghbakhsh,
         "Boublia correlation (g/cm3)" : eixo_densi_boublia
      })
      dict_densidade = df_densidade.to_dict('records')

      df_speed = pd.DataFrame({
         "Temperature (K)" : eixo_temperature,
         "Peyrovedin correlation (m/s)" : eixo_speed,
      })
      dict_speed = df_speed.to_dict('records')

      df_cp = pd.DataFrame({
         "Temperature (K)" : eixo_temperature,
         "Taherzadeh correlation (J/(mol K))" : eixo_cp,
      })
      dict_cp = df_cp.to_dict('records')
      
      return dict_densidade, dict_speed, dict_cp
   
   else:
        return None, None, None



# Calcula a viscosidade e mostra o gráfico e botão
@app.callback(
   Output(component_id='Viscosity', component_property='children'),
   Output(component_id= 'viscosity_dados',  component_property='data'),

   Input(component_id= 'viscosity_button', component_property='n_clicks'),
   State(component_id='critical_des', component_property='data'),

   State(component_id='Ref_temperature', component_property='value'),
   State(component_id='Ref_viscosity', component_property='value'),
   State(component_id='viscosityUnit_ref', component_property='value'),
   
   State(component_id='status', component_property='data'),
   prevent_initial_call=True

)
def prop_visco_lab(n_clicks, des_tabel, 
                   Tk, Vk, unidade_visco, 
                   status):
   #className="btn btn-outline-light btn-lg"

   # Se existir algo
   if status != 'Error Type' and status != 'Error Sum' and status != None:

      if n_clicks > 0:
         df_des = pd.DataFrame(des_tabel)

         Tc = df_des['Tc (K)'][0]
         Pc = df_des['Pc (bar)'][0]

         if Tk  != None and Vk != None:
            
            if Vk > 0 :

               #### Cálculo ######
               # Eixo das viscosidades
               eixo_temperature = np.arange(283.15, 374.15)
               eixo_visco_LS = []
               eixo_visco_Ba = []

               for T in eixo_temperature:
                  if unidade_visco == 'Pa . s':
                     # Viscosity in Pa . s
                     visco_LewisSquires = viscosity_LewisSquires(T, Tk, Vk * 1000) / 1000 # Cp = mPa . s
                     visco_Bakhtyary = viscosity_Bakhtyary(T, Tk, Tc, Pc, Vk) # Pa . s

                     eixo_visco_LS.append(visco_LewisSquires) # Pa . s
                     eixo_visco_Ba.append(visco_Bakhtyary) # Pa . s
                  
                  else: 
                     # Viscosity in mPa . s
                     visco_LewisSquires = viscosity_LewisSquires(T, Tk, Vk) # Cp = mPa . s
                     visco_Bakhtyary = viscosity_Bakhtyary(T, Tk, Tc, Pc, Vk / 1000) * 1000 #Pa . s

                     eixo_visco_LS.append(visco_LewisSquires) # mPa . s
                     eixo_visco_Ba.append(visco_Bakhtyary) # mPa . s
                  

               # Figura
               titulo = ""
               legend = ["Lewis and Squires Correlation", "Bakhtyari Correlation"]

               if unidade_visco == 'Pa . s':
                  y_label = 'Viscosity (Pa . s)'
               else:
                  y_label = 'Viscosity (mPa . s)'
               
               dataframe_visco = pd.DataFrame({
                  "Temperature (K)" : eixo_temperature,
                  f"Lewis and Squires correlation ({unidade_visco})" : eixo_visco_LS,
                  f"Bakhtyari correlation ({unidade_visco})" : eixo_visco_Ba
               })

               dict_visco = dataframe_visco.to_dict('records') #return to save

               figura = Grafico_viscosidade(eixo_temperature, eixo_visco_LS, eixo_visco_Ba, titulo, legenda= legend, eixoY = y_label) #longdash

               # Tela de impressão
               conteudo = html.Div([
                  dcc.Graph(
                     id='visco_grafico',
                     figure=figura,
                     style={"width": "100%",   # ocupa toda a largura
                           "height": "80vh"}   # 80% da altura da tela}
                  )
               ])

               return conteudo, dict_visco


            # Viscosity < 0
            else:
               mensagem = html.P(children = 'Invalid viscosity reference!', style={'color': 'red',
                                                                                                       'fontWeight': 'bold',
                                                                                                       'textAlign': 'left',  
                                                                                                       "fontSize": "1.2em"})

               return mensagem, None

         # Viscosity or temperature incorret
         else:
            mensagem = html.P(children = 'Invalid temperature and viscosity reference!', style={'color': 'red',
                                                                                                       'fontWeight': 'bold',
                                                                                                       'textAlign': 'left',  
                                                                                                       "fontSize": "1.2em"})

            return mensagem, None
      
      # n_clicks = 0
      else:
         raise PreventUpdate

   # Binary DES not reported
   else:
        mensagem = html.P(children = 'The chosen solvent is not a binary or ternary DES!', style={'color': 'red',
                                                                                                       'fontWeight': 'bold',
                                                                                                       'textAlign': 'left',  
                                                                                                       "fontSize": "1.2em"})

        return mensagem, None




############### PRINCIPAL - CALCULOS ###########

# Calcular os valores
@app.callback(
   # Output para cadastrar e mostrar valores
   Output(component_id='Tabela', component_property='children', allow_duplicate= True),

   Output(component_id= 'critical_des',  component_property='data'),
   Output(component_id= 'critical_componentes',  component_property='data'),
   
   Output(component_id= 'status',  component_property='data'),
   
   ######### Inputs ##########
   Input(component_id='critical_button', component_property='n_clicks'),

   State(component_id='Nome_1', component_property='value'),
   State(component_id='Nome_2', component_property='value'),
   State(component_id='Nome_3', component_property='value'),

   State(component_id='fracoes_molares', component_property='data'),
   
   prevent_initial_call=True
)
def obter_dados(n_clicks, name1, name2, name3, fracoes_molares):
   if n_clicks > 0:
      frac_1, frac_2, frac_3 = fracoes_molares


      try:
         float(frac_1)
         float(frac_2)
         float(frac_3)
      
      except:
         mensagem = html.P(children = 'An error occurred, check the molar compositions!', style={'color': 'red',
                                                                                                       'fontWeight': 'bold',
                                                                                                       'textAlign': 'left',  
                                                                                                       "fontSize": "1.2em"})
         
         return mensagem, 'Error Type', 'Error Type', 'Error Type'
      
      if round(frac_1 + frac_2 + frac_3, 6) == 1:          
         names = [name1, name2, name3]
         X = [frac_1, frac_2, frac_3]

         df_comp, df_des = PropriedadesDes(names, X)

         try:
            count_nulo = df_comp['Abr.'].value_counts()['/']
         except:
            count_nulo = 0

         # Se houver 2 ou 3 componentes:
         if count_nulo <= 1:
            status = 1

            dict_comp = df_comp.to_dict('records') # list of dicts
            dict_des = df_des.to_dict('records') # list of dicts

         # Se tiver somente 1
         else:
            status = None

            dict_comp = df_comp.to_dict('records') # list of dicts
            dict_des = df_comp[df_comp['Abr.'] != '/'].to_dict('records') # list of dicts


         ## Preparando a mensagem da tela
         
         conteudo = html.Div([ 
            html.Hr(),
            html.Br(),

            html.P(children = 'The critical properties of the components are:', style={'textAlign': 'left', "fontSize": "1.2em"}),

            dash_table.DataTable(
               data = round(pd.DataFrame(dict_comp), 4).to_dict('records'), #List of dict
               columns = [
                  {"name": i, 
                  "id": i, 
                  } for i in df_comp.columns],
               style_cell={
                  'fontSize': '18px',
                  'textAlign': 'center',      # alinhamento horizontal
                  'color': 'black',           # cor da fonte
               'backgroundColor': 'white', # cor do fundo da célula
               },

               style_header={
                  'fontWeight': 'bold',
                  'backgroundColor': "#abfcff",
                  'fontSize': '20px',
                  'color': 'black',
               }
            ),

            html.Br(),
            html.P(children = 'The critical properties of DES is:', style={'textAlign': 'left', "fontSize": "1.2em"}),

            dash_table.DataTable(
               data = round(pd.DataFrame(dict_des), 4).to_dict('records'), #List of dict
               columns = [
                  {"name": i, 
                  "id": i, 
                  } for i in pd.DataFrame(dict_des).columns],
               
               style_cell={
                  'fontSize': '18px',
                  'textAlign': 'center',      # alinhamento horizontal
                  'color': 'black',           # cor da fonte
               'backgroundColor': 'white', # cor do fundo da célula
               },

               style_header={
                  'fontWeight': 'bold',
                  'backgroundColor': "#abfcff",
                  'fontSize': '20px',
                  'color': 'black',
               }
            ),

            html.Br(),

            # Botão de download
            dbc.Button(children="Download CSV", id='Botao_download', n_clicks=0, outline=True, color="dark", size = 'lg',
                        className=" mx-2"),
            dbc.Tooltip("Download a file with the calculated data", target="Botao_download"),
            

            dcc.Link("Correlations", id = "Link_correlation", href="/pages/tela_propriedade", className="btn btn-outline-secondary btn-lg disabled"),
            dbc.Tooltip("Uses empirical correlations to calculate properties of binary and ternary DES", target="Link_correlation"),

            dcc.Download(id="download_Resultados"),
            html.Br(),
         ])

         # Armazenamos os dados na forma de dicionarios
         return conteudo, dict_des, dict_comp, status
      
      else:
         mensagem = html.P(children = 'An error occurred: the total mole fraction must equal 1.', style={'color': 'red',
                                                                                                       'fontWeight': 'bold',
                                                                                                       'textAlign': 'left',  
                                                                                                       "fontSize": "1.2em"})
         
         return mensagem, 'Error Sum', 'Error Sum', 'Error Sum'

   else:
      return dash.no_update


# Mostrar valores
@app.callback(
   # Output para cadastrar e mostrar valores
   Output(component_id='Tabela', component_property='children'),

   # Verificar se existe valores já cadastrados
   Input(component_id='critical_des', component_property='data'),
   Input(component_id='critical_componentes', component_property='data'),
   Input(component_id='url_page', component_property='data')
)
def mostrar(des_tabel, comp_tabel, local):

   if local == 'data':

      if des_tabel != 'Error Type' and des_tabel != 'Error Sum' and des_tabel != None:

         df_des = pd.DataFrame(des_tabel)
         df_comp = pd.DataFrame(comp_tabel)

         try:
            count_nulo = df_comp['Abr.'].value_counts()['/']
         except:
            count_nulo = 0

         # Se houver 2 ou 3 componentes:
         if count_nulo <= 1:

            dict_comp = df_comp.to_dict('records') # list of dicts
            dict_des = df_des.to_dict('records') # list of dicts
         
         else:
            dict_comp = df_comp.to_dict('records') # list of dicts
            dict_des = df_comp[df_comp['Abr.'] != '/'].to_dict('records') # list of dicts


         conteudo = html.Div([ 

            html.Hr(),
            html.Br(),

            html.P(children = 'The critical properties of the components are:', style={'textAlign': 'left', "fontSize": "1.2em"}),

            dash_table.DataTable(
               data = round(pd.DataFrame(dict_comp), 4).to_dict('records'), #List of dict
               columns = [
                  {"name": i, 
                  "id": i, 
                  } for i in df_comp.columns],
               style_cell={
                  'fontSize': '18px',
                  'textAlign': 'center',      # alinhamento horizontal
                  'color': 'black',           # cor da fonte
               'backgroundColor': 'white', # cor do fundo da célula
               },

               style_header={
                  'fontWeight': 'bold',
                  'backgroundColor': "#abfcff",
                  'fontSize': '20px',
                  'color': 'black',
               }
            ),

            html.Br(),
            html.P(children = 'The critical properties of DES is:', style={'textAlign': 'left', "fontSize": "1.2em"}),

            dash_table.DataTable(
               data = round(pd.DataFrame(dict_des), 4).to_dict('records'), #List of dict
               columns = [
                  {"name": i, 
                  "id": i, 
                  } for i in pd.DataFrame(dict_des).columns],
               
               style_cell={
                  'fontSize': '18px',
                  'textAlign': 'center',      # alinhamento horizontal
                  'color': 'black',           # cor da fonte
               'backgroundColor': 'white', # cor do fundo da célula
               },

               style_header={
                  'fontWeight': 'bold',
                  'backgroundColor': "#abfcff",
                  'fontSize': '20px',
                  'color': 'black',
               }
            ),

            html.Br(),

            # Botão de download
            dbc.Button(children="Download CSV", id='Botao_download', n_clicks=0, outline=True, color="dark", size = 'lg',
                        className="mx-2"),
            dbc.Tooltip("Download a file with the calculated data", target="Botao_download"),

            dcc.Link("Correlations", id = "Link_correlation", href="/pages/tela_propriedade", className="btn btn-outline-secondary btn-lg disabled"),
            dbc.Tooltip("Uses empirical correlations to calculate properties of binary and ternary DES", target="Link_correlation"),


            dcc.Download(id="download_Resultados"),
            html.Br(),
   ])
         
         return conteudo

      elif des_tabel == 'Error Type':
         mensagem = html.P(children = 'An error occurred, check the molar compositions and temperature reported!', style={'color': 'red',
                                                                                                         'fontWeight': 'bold',
                                                                                                         'textAlign': 'left',  
                                                                                                         "fontSize": "1.2em"})

         return mensagem

      elif des_tabel == 'Error Sum':
         mensagem = html.P(children = 'An error occurred: the total mole fraction must equal 1.', style={'color': 'red',
                                                                                                         'fontWeight': 'bold',
                                                                                                         'textAlign': 'left',  
                                                                                                         "fontSize": "1.2em"})
         return mensagem
      
      

   else:
      raise PreventUpdate




################ DOWNLOAD DO CSV #################
@app.callback(
    Output(component_id = 'download_Resultados', component_property = 'data'),

    Input(component_id= 'Botao_download', component_property = 'n_clicks'),

    State(component_id= 'critical_des', component_property='data'),
    State(component_id= 'critical_componentes', component_property='data'),

    # Não será chamado automaticamento no inicio
    prevent_initial_call=True

)
def download_csv(n_click_download,
                 crit_des, crit_comp,
                 ):

    if n_click_download > 0:
      df_comp = pd.DataFrame(crit_comp)
      df_des = pd.DataFrame(crit_des)
      
      # rename
      df_comp.rename(columns={'ω': 'acentric factor'}, inplace = True)
      df_des.rename(columns={'ω': 'acentric factor'}, inplace = True)

      str1 = "Web App to Critical Properties;Universidade Federal Ceará;LTS;\nEncoding:;utf-8\nThis application was developed by Quinto F. H. B from the Laboratory of Thermodynamics and Separation Processes (LTS)\n"
      str2 = df_comp.to_csv(sep=';', index=False, encoding='utf-8-sig')
      str3 = df_des.to_csv(sep=';', index=False, encoding='utf-8-sig')
      str4 = df_references.to_csv(sep=';', index=False, encoding='utf-8')

      texto = str1 + "\n'=== Components ===;\n" + str2 + "\n'=== DES ===;\n" + str3 + "\n'=== ## ===;\n" + str4

      return dcc.send_string(texto, "Critical_Properties_DES.csv")


    else:
        raise PreventUpdate




@app.callback(
    Output(component_id = 'download_Resultados_correlations', component_property = 'data'),

    Input(component_id= 'button_csv_correlations', component_property = 'n_clicks'),
    
    State(component_id= 'viscosity_dados', component_property='data'),
    State(component_id= 'density_dados', component_property='data'),
    State(component_id= 'speed_dados', component_property='data'),
    State(component_id= 'cp_dados', component_property='data'),

    State(component_id= 'critical_des', component_property='data'),
    State(component_id= 'critical_componentes', component_property='data'),

    # Não será chamado automaticamento no inicio
    prevent_initial_call=True

)
def download_csv_correlation(n_click_download, 
                             dict_visco, dict_dens, dict_speed, dict_cp,
                             crit_des, crit_comp,
                           ):

    if dict_dens != None:

      if n_click_download > 0:

         df_dens = pd.DataFrame(dict_dens)
         df_speed = pd.DataFrame(dict_speed)
         df_cp = pd.DataFrame(dict_cp)

         df_comp = pd.DataFrame(crit_comp)
         df_des = pd.DataFrame(crit_des)

         #rename acentric
         df_comp.rename(columns={'ω': 'acentric factor'}, inplace = True)
         df_des.rename(columns={'ω': 'acentric factor'}, inplace = True)

         str1 = "Web App to Critical Properties;Universidade Federal Ceará;LTS;\nEncoding:;utf-8\nThis application was developed by Quinto F. H. B from the Laboratory of Thermodynamics and Separation Processes (LTS)\n"
         
         strCompo = df_comp.to_csv(sep=';', index=False, encoding='utf-8-sig')
         strDES = df_des.to_csv(sep=';', index=False, encoding='utf-8-sig')
         strRef = df_references.to_csv(sep=';', index=False, encoding='utf-8-sig')

         str_Density = df_dens.to_csv(sep=';', index=False, encoding='utf-8-sig')
         str_Speed = df_speed.to_csv(sep=';', index=False, encoding='utf-8-sig')
         str_cp = df_cp.to_csv(sep=';', index=False, encoding='utf-8-sig')


         if dict_visco == None:
            texto = str1 + "\n'=== Components ===;\n" + strCompo + "\n'=== DES ===;\n" + strDES + "\n'=== Estimate Density ===;\n" + str_Density + "\n'=== Estimate Speed ===;\n" + str_Speed + "\n'=== Estimate Cp ===;\n" + str_cp + "\n'=== ## ===;\n" + strRef

         else:
            df_visco = pd.DataFrame(dict_visco)

            strVisco = df_visco.to_csv(sep=';', index=False, encoding='utf-8-sig')

            texto = str1 + "\n'=== Components ===;\n" + strCompo + "\n'=== DES ===;\n" + strDES + "\n'=== Estimate Density ===;\n" + str_Density + "\n'=== Estimate Speed ===;\n" + str_Speed + "\n'=== Estimate Cp ===;\n" + str_cp + "\n'=== Estimate Viscosity ===;\n" + strVisco + "\n'=== ## ===;\n" + strRef

         return dcc.send_string(texto, "correlation_Properties_DES.csv")


    else:
        raise PreventUpdate


# Final, executando
if __name__ == '__main__':
    app.run(debug=True)
