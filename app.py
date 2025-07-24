# Importando as bibliotecas
from dash import Dash, html, dcc, State, dash_table, ctx
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash

# Importa a função que calcula as propriedades do DES
from dados.Funcoes import PropriedadesDes, Get_components, Density_Boublia, Density_Haghbakhsh

# Usado na manipulação de matrizes
import numpy as np

# Usada para fazer download do csv
import pandas as pd

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


    # Armazena as variáveis "ocultas" que será usada para os gráficos
    dcc.Store(id = 'Temperature_store',  storage_type = 'session'), # Armazena Aij
    dcc.Store(id = 'TemperatureUnit_store',  storage_type = 'session'), # Armazena Alfa
    
    dcc.Store(id = 'critical_des',  storage_type = 'session'),
    dcc.Store(id = 'critical_componentes',  storage_type = 'session'),

    dcc.Store(id = 'Density_Haghbakhsh', storage_type = 'session'),
    dcc.Store(id = 'Density_Boublia', storage_type = 'session'),

    dcc.Store(id = 'fracoes_molares', storage_type = 'session')
],fluid=True)


##################### CALLBACKS PRINCIPAL #####################
# Armazenamento das frac
# Edição se ternário
@app.callback(
    # Recebendo os valores na tela
    Output(component_id='fracoes_molares', component_property='data'),

    Input(component_id='frac_1', component_property='value'),
    Input(component_id='frac_2', component_property='value'),
    Input(component_id='frac_3', component_property='value'),
)
def save_frac(x1, x2, x3):
   valores = [x1, x2, x3]

   return valores


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

   if '/' in nomes:
      
      for indice, valor in enumerate(nomes):
         if nomes[indice] == '/':
            estados[indice] = True
            valores[indice] = 0
         else:
            pass

      return estados[0], estados[1], estados[2], valores[0], valores[1], valores[2]

   else:
      raise PreventUpdate


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

      # Se houver 2 ou 3 componentes:
      if df_comp['Abr.'].value_counts()['/'] <= 1:
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


# Mostrar as densidades
@app.callback(
   Output(component_id='Propriedade', component_property='children'),

   Input(component_id= 'Density_Haghbakhsh', component_property='data'),
   Input(component_id= 'Density_Boublia', component_property='data'),
   State(component_id='critical_des', component_property='data'),
   State(component_id='Temperature_store', component_property='data'),
   State(component_id='TemperatureUnit_store', component_property='data'),

)
def prop_lab(densi_Haghbakhsh, densi_Boublia, des_tabel, temperature, temp_uni):
   #className="btn btn-outline-light btn-lg"

   # Se existir algo
   if densi_Haghbakhsh != 'Error Type' and densi_Haghbakhsh != 'Error Sum' and densi_Haghbakhsh != None:

      df_des = pd.DataFrame(des_tabel)

      conteudo = html.Div([ 


         html.P(children = f'For the informed system, at {temperature} {temp_uni}:', style={'textAlign': 'left', "fontSize": "1.2em"}),

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
      html.P(children = 'The following values were obtained:', style={'textAlign': 'left', "fontSize": "1.2em"}),

      html.Div([
                  html.Strong("Density (Haghbakhsh Correlation): "),
                  html.Span(f"{densi_Haghbakhsh:.5f} g/cm³")
            ], style={"marginBottom": "10px"}),

            html.Div([
                  html.Strong("Density (Boublia Correlation): "),
                  html.Span(f"{densi_Boublia:.5f} g/cm³")
            ], style={"marginBottom": "10px"}),

            html.Div([
                  html.Strong("Relative Percentage Error (relative a Haghbakhsh): "),
                  html.Span(f"{(abs(densi_Boublia - densi_Haghbakhsh) / densi_Haghbakhsh) * 100:.4f} %")
            ]),

])
      
      return conteudo
   
   else:
        mensagem = html.P(children = 'The chosen solvent is not a binary or ternary DES!', style={'color': 'red',
                                                                                                       'fontWeight': 'bold',
                                                                                                       'textAlign': 'left',  
                                                                                                       "fontSize": "1.2em"})

        return mensagem



# Calcular os valores
@app.callback(
   # Output para cadastrar e mostrar valores
   Output(component_id='Tabela', component_property='children', allow_duplicate= True),

   Output(component_id= 'critical_des',  component_property='data'),
   Output(component_id= 'critical_componentes',  component_property='data'),
   Output(component_id= 'Temperature_store',  component_property='data'),
   Output(component_id= 'TemperatureUnit_store',  component_property='data'),

   Output(component_id= 'Density_Haghbakhsh',  component_property='data'),
   Output(component_id= 'Density_Boublia',  component_property='data'),

   Input(component_id='critical_button', component_property='n_clicks'),

   State(component_id='Nome_1', component_property='value'),
   State(component_id='Nome_2', component_property='value'),
   State(component_id='Nome_3', component_property='value'),
   
   State(component_id='frac_1', component_property='value'),
   State(component_id='frac_2', component_property='value'),
   State(component_id='frac_3', component_property='value'),
   
   State(component_id= 'Temperature', component_property='value'),
   State(component_id= 'TemperatureUnit', component_property='value'),
   prevent_initial_call=True
)
def obter_dados(n_clicks, name1, name2, name3, frac_1, frac_2, frac_3, temperature, temp_unit):

   if n_clicks > 0:
      try:
         float(frac_1)
         float(frac_2)
         float(frac_3)
         float(temperature)
      
      except:
         mensagem = html.P(children = 'An error occurred, check the molar compositions and temperature reported!', style={'color': 'red',
                                                                                                       'fontWeight': 'bold',
                                                                                                       'textAlign': 'left',  
                                                                                                       "fontSize": "1.2em"})
         return mensagem, 'Error Type', 'Error Type', 'Error Type', 'Error Type', 'Error Type', 'Error Type'
      
      if frac_1 + frac_2 + frac_3 == 1:          
         names = [name1, name2, name3]
         X = [frac_1, frac_2, frac_3]

         df_comp, df_des = PropriedadesDes(names, X)

         # Se houver 2 ou 3 componentes:
         if df_comp['Abr.'].value_counts()['/'] <= 1:

            dict_comp = df_comp.to_dict('records') # list of dicts
            dict_des = df_des.to_dict('records') # list of dicts

            # Propriedades para calcular a densidade
            Mw = df_des['Mw (g/mol)'][0]
            Vc = df_des['Vc (mL/mol)'][0]
            Tc = df_des['Tc (K)'][0]
            Pc = df_des['Pc (bar)'][0]
            w =  df_des['ω'][0]
            densi_Haghbakhsh = Density_Haghbakhsh(temperature, Tc, Vc, w)
            densi_Boublia = Density_Boublia(temperature, Mw, Tc, Vc, Pc, w)
         
         # Se tiver somente 1
         else:
            dict_comp = df_comp.to_dict('records') # list of dicts
            dict_des = df_comp[df_comp['Abr.'] != '/'].to_dict('records') # list of dicts

            densi_Haghbakhsh = None
            densi_Boublia = None

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

            dcc.Link("Correlations", id = "Link_correlation", href="/pages/tela_propriedade", className="btn btn-outline-secondary btn-lg disabled"),
            dbc.Tooltip("Uses empirical correlations to calculate properties of binary and ternary DES", target="Link_correlation"),

            dcc.Download(id="download_Resultados"),
            html.Br(),
         ])

         # Armazenamos os dados na forma de dicionarios
         return conteudo, dict_des, dict_comp, temperature, temp_unit, densi_Haghbakhsh, densi_Boublia
      
      else:
         mensagem = html.P(children = 'An error occurred: the total mole fraction must equal 1.', style={'color': 'red',
                                                                                                       'fontWeight': 'bold',
                                                                                                       'textAlign': 'left',  
                                                                                                       "fontSize": "1.2em"})
         
         return mensagem, 'Error Sum', 'Error Sum', 'Error Sum', 'Error Sum', 'Error Sum', 'Error Sum'
   
   else:
      return dash.no_update


# Mostrar valores
@app.callback(
   # Output para cadastrar e mostrar valores
   Output(component_id='Tabela', component_property='children'),

   Input(component_id='critical_button', component_property='n_clicks'),
   # Verificar se existe valores já cadastrados
   Input(component_id='critical_des', component_property='data'),
   Input(component_id='critical_componentes', component_property='data'),
)
def mostrar(n_clicks, des_tabel, comp_tabel):

   #if ctx.triggered_id == "critical_button":

   if des_tabel != 'Error Type' and des_tabel != 'Error Sum' and des_tabel != None:

      df_des = pd.DataFrame(des_tabel)
      df_comp = pd.DataFrame(comp_tabel)


      # Se houver 2 ou 3 componentes:
      if df_comp['Abr.'].value_counts()['/'] <= 1:

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



################ DOWNLOAD DO CSV #################
@app.callback(
    Output(component_id = 'download_Resultados', component_property = 'data'),

    Input(component_id= 'Botao_download', component_property = 'n_clicks'),

    State(component_id= 'critical_des', component_property='data'),
    State(component_id= 'critical_componentes', component_property='data'),
    State(component_id= 'Temperature_store',  component_property='data'),
    State(component_id= 'TemperatureUnit_store',  component_property='data'),

    # Não será chamado automaticamento no inicio
    prevent_initial_call=True

)
def download_csv(n_click_download,
                 crit_des, crit_comp,
                 temp, tempUnit):

    if n_click_download > 0:
      df_comp = pd.DataFrame(crit_comp)
      df_des = pd.DataFrame(crit_des)


      str1 = "Web App to Critical Properties;Universidade Federal Ceará;LTS;\n"
      str2 = df_comp.to_csv(sep=';', index=False, encoding='utf-8-sig')
      str3 = df_des.to_csv(sep=';', index=False, encoding='utf-8-sig')

      texto = str1 + f"System Temperature:;{temp};{tempUnit};\n" + "\n=== Components ===;\n" + str2 + "\n=== DES ===;\n" + str3

      return dcc.send_string(texto, "Critical_Properties_DES.csv")


    else:
        raise PreventUpdate


# Final, executando
if __name__ == '__main__':
    app.run(debug=True)
