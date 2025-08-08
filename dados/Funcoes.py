import pandas as pd
import numpy as np
import os
# Biblioteca para plotar gráficos interativos
import plotly.express as px
import plotly.graph_objects as go

caminho_base = os.path.dirname(__file__)  # caminho da pasta 'dados'

def CriarArquivo():

    df_comp = pd.read_excel(os.path.join(caminho_base, 'Composicoes.xlsx'))
    df_prop = pd.read_excel(os.path.join(caminho_base, 'Propriedades.xlsx'))

    grupos = df_comp.columns[1:]

    dicionario = []

    for linha in range(len(df_comp)):
        name = df_comp['Abr.'][linha]

        if name != 'water' and name != '/':
            zi = np.array(df_comp[grupos].iloc[linha]) #number of occurrences of group

            delta_Mi = df_prop[df_prop['Propriedade'] == '∆Mi'][grupos]  #Values ∆Mi of group
            delta_Mi = np.array(delta_Mi).reshape(47,)

            delta_Tb = df_prop[df_prop['Propriedade'] == '∆TbMi'][grupos]
            delta_Tb = np.array(delta_Tb).reshape(47,)

            delta_Vc = df_prop[df_prop['Propriedade'] == '∆VcMi'][grupos]  
            delta_Vc = np.array(delta_Vc).reshape(47,)

            delta_Pc =  df_prop[df_prop['Propriedade'] == '∆PcMi'][grupos]
            delta_Pc = np.array(delta_Pc).reshape(47,)

            delta_Tc = df_prop[df_prop['Propriedade'] == '∆TcMi'][grupos] 
            delta_Tc = np.array(delta_Tc).reshape(47,)

            zi_deltaTc = sum(zi * delta_Tc)
            zi_deltaPc = sum(zi * delta_Pc)
            
            M = sum(zi *  delta_Mi)
            Tb = 198.2 + sum(zi * delta_Tb)
            Vc = 6.75 + sum(zi * delta_Vc)
            
            Tc = Tb / (0.5703 + 1.0121 * zi_deltaTc - pow(zi_deltaTc, 2))
            
            Pc = M / pow(0.2573 + zi_deltaPc, 2)


            w1 = ((Tb - 43) * (Tc - 43)) / ((Tc - Tb) * (0.7*Tc - 43)) * np.log10(Pc/1.01325)
            w2 = ((Tc - 43) / (Tc - Tb)) * np.log10(Pc / 1.01325)
            w3 = np.log10(Pc/1.01325) - 1

            w = w1 - w2 + w3

            dici = {
                'Abr.' : name,
                'Mw (g/mol)' : M,
                'Vc (mL/mol)' : Vc,
                'Tc (K)' : Tc,
                'Pc (bar)' : Pc,
                'ω' : w
            }

            dicionario.append(dici)

        
        elif name == '/':
            dici = {
                'Abr.' : name,
                'Mw (g/mol)' : 0,
                'Vc (mL/mol)' : 0,
                'Tc (K)' : 0,
                'Pc (bar)' : 0,
                'ω' : 0
            }

            dicionario.append(dici)        

        
        else:
            dici = {
                'Abr.' : name,
                'Mw (g/mol)' : 18.015,
                'Vc (mL/mol)' : 55.900,
                'Tc (K)' : 647.100,
                'Pc (bar)' : 220.550,
                'ω' : 0.345
            }

            dicionario.append(dici)

    df_final = pd.DataFrame(dicionario)
    df_final.head()

    # Correto
    df_final.to_excel(os.path.join(caminho_base, 'Valores.xlsx'), index=False)


def Matriz_Vcnm(Vc):
    
    V11 = 1/8 * ( pow( pow(Vc[0], 1/3) + pow(Vc[0], 1/3), 3) )
    V22 = 1/8 * ( pow( pow(Vc[1], 1/3) + pow(Vc[1], 1/3), 3) )
    V33 = 1/8 * ( pow( pow(Vc[2], 1/3) + pow(Vc[2], 1/3), 3) )

    V12 = 1/8 * ( pow( pow(Vc[0], 1/3) + pow(Vc[1], 1/3), 3) )
    V13 = 1/8 * ( pow( pow(Vc[0], 1/3) + pow(Vc[2], 1/3), 3) )
    V23 = 1/8 * ( pow( pow(Vc[1], 1/3) + pow(Vc[2], 1/3), 3) )

    matriz = np.array([
        [V11,  V12,    V13],
        [0,    V22,    V23],
        [0,    0,      V33]
    ])

    return matriz


def Matriz_Tcm(Tc):
    T11 = np.sqrt(Tc[0] * Tc[0])
    T22 = np.sqrt(Tc[1] * Tc[1])
    T33 = np.sqrt(Tc[2] * Tc[2])

    T12 = np.sqrt(Tc[0] * Tc[1])
    T13 = np.sqrt(Tc[0] * Tc[2])
    T23 = np.sqrt(Tc[1] * Tc[2])

    matriz = np.array([
        [T11, T12, T13],
        [0,   T22, T23],
        [0,   0,   T33]
    ])

    return matriz

def Get_components():
    df = pd.read_excel(os.path.join(caminho_base, 'Valores.xlsx'))
    return df['Abr.'].unique()


def PropriedadesDes(names, X):

    qnt_nulos = names.count('/')

    # Tra
    X = np.array(X)

    # Acessando o Dataframe
    df = pd.read_excel(os.path.join(caminho_base, 'Valores.xlsx'))

    # Coloca a coluna 'Abr.' como indice e filtra os valores, depois reseta o indice da matriz filtrada
    df_filtrada = df.set_index('Abr.').loc[names].reset_index()

    Mwi = np.array(df_filtrada['Mw (g/mol)'])
    Vci = np.array(df_filtrada['Vc (mL/mol)'])
    Tci = np.array(df_filtrada['Tc (K)'])
    Pci = np.array(df_filtrada['Pc (bar)'])
    Wci = np.array(df_filtrada['ω'])

    # Matrizes
    Vcm = Matriz_Vcnm(Vci)
    Tcm = Matriz_Tcm(Tci)

        
    ####### Calculo das propriedades dos DES #######
    if qnt_nulos <= 1: 
        Mdes = sum(X * Mwi)

        Vcdes = X[0] * X[0] * Vcm[0][0] + X[1] * X[1] * Vcm[1][1] + X[2] * X[2] * Vcm[2][2] + 2 * X[0] * X[1] * Vcm[0][1] + 2 * X[0] * X[2] * Vcm[0][2] + 2 * X[1] * X[2] * Vcm[1][2]

        Tcdes_1 = X[0] * X[0] * pow(Vcm[0][0], 0.25) * Tcm[0][0] + X[1] * X[1] * pow(Vcm[1][1], 0.25) * Tcm[1][1] +  X[2] * X[2] * pow(Vcm[2][2], 0.25) * Tcm[2][2]

        Tcdes_2 = 2 * X[0] * X[1] * pow(Vcm[0][1], 0.25) * Tcm[0][1] + 2 * X[0] * X[2] * pow(Vcm[0][2], 0.25) * Tcm[0][2] +  2 * X[1] * X[2] * pow(Vcm[1][2], 0.25) * Tcm[1][2]

        Tcdes = (1 / pow(Vcdes, 0.25)) * (Tcdes_1 + Tcdes_2)

        Wdes = sum(X * Wci)

        Pcdes = (0.2905 - 0.0850 * Wdes) * (83.1447 * Tcdes) / Vcdes
    
    elif qnt_nulos == 2:

        component = [n_nulo for n_nulo in names if n_nulo != "/"] # Componente diferente de "/"

        df_component = df_filtrada[ df_filtrada['Abr.'] == component[0]]

        Mdes = np.array(df_component['Mw (g/mol)'])[0]
        
        Vcdes = np.array(df_component['Vc (mL/mol)'])[0]

        Tcdes = np.array(df_component['Tc (K)'])[0]

        Wdes = np.array(df_component['ω'])[0]

        Pcdes = np.array(df_component['Pc (bar)'])[0]

    
    else:
        df_component = df[df['Abr.'] == '/']

        Mdes = np.array(df_component['Mw (g/mol)'])[0]

        Vcdes = np.array(df_component['Vc (mL/mol)'])[0]

        Tcdes = np.array(df_component['Tc (K)'])[0]

        Wdes = np.array(df_component['ω'])[0]

        Pcdes = np.array(df_component['Pc (bar)'])[0]


    df_des = pd.DataFrame([{
        'Components' : f'{names[0]} | {names[1]} | {names[2]}',
        'X1:X2:X3' : f'{X[0]}:{X[1]}:{X[2]}',
        'Mw (g/mol)': Mdes,
        'Vc (mL/mol)': Vcdes,
        'Tc (K)' : Tcdes,
        'Pc (bar)' : Pcdes,
        'ω' : Wdes
    }])

    return df_filtrada, df_des


def Density_Haghbakhsh(T, Tc, Vc, w):
    """
    Função que retorna a densidade de acordo com a correlação de Haghbakhsh. Des de 283.15 K até 373.15 K.

    Parâmetros
    ----------
    T | Float
        Temperatura em K
    Pc | Float (Bar)
        Pressão Crítica
    Tc | Float
        Temperatura Crítica
    Vc | Float
        Volume molar
    M | Float
        Massa Molar (g/mol)
    w | Float
        Fator acêntrico
    R | Float
        Constante dos gases ideais J / (⋅mol K) .

    Retorna
    ----------
    Densidade
    """

    A1 = - 1.13e-6
    A2 = 2.566e-3
    A3 = 0.2376
    A4 = -4.67e-4
    B = -4.64e-4

    A = A1 * pow(Tc, 2) + A2 * Tc + A3 * pow(w, 0.2211) + A4 * Vc
    densidade = A + B * T

    return densidade


def Density_Boublia(T, MM, Tc, Vc, Pc, w):
    """
    Função que retorna a densidade de acordo com a correlação de Boublia et al. (2023), para sistemas ternários. Aplicou na faixa de 273.15 até 373.15 K.

    Parâmetros
    ----------
    T | Float
        Temperatura em K
    Pc | Float Bar
        Pressão Crítica
    Tc | Float
        Temperatura Crítica
    Vc | Float
        Volume molar
    M | Float
        Massa Molar (g/mol)
    w | Float
        Fator acêntrico
    R | Float
        Constante dos gases ideais J / (⋅mol K) .

    Retorna
    ----------
    Densidade
    """

    A = -4.717e-7
    B =  9.098e-4
    C =  7.1965e-2
    D = -2.034e-3
    E = -6.540e-4
    F = -6.051e-5
    G = 6.1911e-3

    densidade = A * pow(Tc, 2) + B * Tc + C * pow(w, 0.67131) + D * Vc + E * T + F * Pc + G * MM + 0.8597

    return densidade


def Speed_Peyrovedin(T, MM, Vc, w):
    """
    Função que retorna a velocidade do som usando a correlação de Peyrovedin et al. (2020). Criada para DES Binários na faixa 278.15 até 363.15 K.

    Parâmetros
    ----------
    T | Float
        Temperatura em K
    Vc | Float
        Volume molar
    M | Float
        Massa Molar (g/mol)
    w | Float
        Fator acêntrico

    Retorna
    ----------
    Cp (J/mol K)
    """
    #bar para MPa


    u = w * (7.378 * MM - 2.012 * T) - 2.911 * Vc + 2514.2

    return u


def Cp_Mehrdad(T, MM, Pc_bar, w):
    """
    Função que retorna Cp usando a correlação de Mehrdad et al. (2020). Criada para DES Binários na faixa 278.15 até 363.15 K.

    Parâmetros
    ----------
    T | Float
        Temperatura em K
    Pc | Float (Bar)
        Pressão Crítica
    Tc | Float
        Temperatura Crítica
    Vc | Float
        Volume molar
    M | Float
        Massa Molar (g/mol)
    w | Float
        Fator acêntrico
    R | Float
        Constante dos gases ideais J / (⋅mol K) .

    Retorna
    ----------
    Cp (J/mol K)
    """
    #bar para MPa
    Pc = Pc_bar / 10

    A1 = 3.8e-4
    A2 = 6.3e-5
    A3 = -24577.4
    A4 = -94.9
    B = 132.27

    A = A1 * (pow(MM, 3) / pow(Pc, 6)) + A2 * pow(MM, 2 * w) + (A3 / MM) + A4

    Cp = A + B * pow(T, 1/4)

    return Cp


def viscosity_LewisSquires(T, Tk, visco_k):
    ''' For organic compounds and conventional liquids, Lewis and Squires [61] had proposed a global viscosity correlation to calculate the viscosities at atmospheric pressure

    -----------------
    T : Temperature (K)
    Tk : Temperature Reference (K)
    vico_K: Viscosity in temperature reference (cP)
    '''
    visc = pow(visco_k, -0.2661) + (T - Tk) / 233

    viscosidade = pow(visc, -1/0.2661)

    return viscosidade


def viscosity_Haghbakhsh_Raeissi(T, Tk, visco_k, Mw):
    '''
    Haghbakhsh and Raeissi for estimating the liquid viscosities of 1-alkyl-3-methylimidazolium ionic liquids at different temperatures and atmospheric pressure.

    ------------
    T : Temperature (K)
    Tk : Temperature reference (K)
    visco_K : Viscosity in temperature reference (Pa.s)
    Mw : Molecular weight
    '''
    A = -0.3652558 + 0.00032588 * Mw
    B = 9.0638325 + 0.11681607 * Mw

    viscosidade = pow( pow(visco_k, A) + (T - Tk)/B, 1/A)

    return viscosidade


def viscosity_Bakhtyary(T, Tk, Tc, Pc, visco_k):
    '''
    Bakhtyari A. et al. developed a general model to estimate the viscosity of binary DES, using 1308 experimental data, and 156 DES. It requires Pc, Tc and a reference date.

    ------------
    T : Temperature (K)
    Tk : Temperature reference (K)
    Tc : Critical Temperature (K)
    Pc : Critical Pressure (bar)
 
    visco_K : Viscosity in temperature reference (Pa.s)
    '''
    A = -0.817/Pc - 0.123
    B = -1.595 * Tc

    viscosidade = pow( pow(visco_k, A) + B * ((Tk - T) / (T * Tk)), 1/A)

    return viscosidade


def Grafico_viscosidade(eixo_t, eixo_visco1, 
                        eixo_visco_2, titulo, 
                        legenda = ["correlation 1", "correlation 2"], 
                        tipo = 'solid', 
                        cor = ['black', 'red'],
                        eixoX = 'Temperature (K)',
                        eixoY = 'Viscosity (mPa . s)'):
    
    """
    Função para o gráfico da viscosidade
    """
    
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x = eixo_t, 
                y = eixo_visco1, 
                mode='lines', 
                name= legenda[0], 
                marker = dict(symbol = 'circle', size = 10, color = cor[0], opacity = 1), 
                line = dict(dash = tipo, color = cor[0]) # solid, dot, dash, longdash
                )
    )

    fig.add_trace(
        go.Scatter(x = eixo_t, 
                y = eixo_visco_2, 
                mode='lines', 
                name= legenda[1], 
                marker = dict(symbol = 'circle', size = 10, color = cor[1], opacity = 1), 
                line = dict(dash = tipo, color = cor[1]) # solid, dot, dash, longdash
                )
    )

    fig.update_layout(
        width=1000, height=700, plot_bgcolor='white',
        title={
            'text': titulo,
            'y': 0.9,  # Posição horizontal (0=esquerda, 1=direita)
            'x': 0.5,  # Posição vertical (0=embaixo, 1=em cima)
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 20, 'family': 'Arial', 'color': 'black', 'weight': 'bold'}
        },

        xaxis={
            'title': eixoX,
            'tickformat': '.1f'},

        yaxis={
            'title': eixoY,
            'tickformat': '.2f'},

        font={
            'family': 'Arial',
            'size': 18,
            'color': 'black'},

        legend=dict(
            x=0.7,  # Posição horizontal (0=esquerda, 1=direita)
            y=1,  # Posição vertical (0=embaixo, 1=em cima)
            bgcolor='rgba(255, 255, 255, 0.5)',  # Fundo da legenda com transparência
            bordercolor='black',  # Cor da borda
            borderwidth=2  # Largura da borda
        ),

        showlegend = True
    )


    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray', showline=True, linecolor='black')

    if max(eixo_visco1) < 1000 or max(eixo_visco_2) < 5000:
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray', showline=True, linecolor='black')

    else: 
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray', showline=True, linecolor='black', exponentformat="E", showexponent="all", tickformat=".2e")



    return fig


referencias = [
    r'Alvarez, V. H.; Valderrama, J. O. A modified Lydersen-Joback-Reid method to estimate the critical properties of biomolecules. Alimentaria. 2004, 254,55-66',
    
    r"Bakhtyari, A., Haghbakhsh, R., Duarte, A. R. C., & Raeissi, S. (2020). A simple model for the viscosities of deep eutectic solvents. Fluid Phase Equilibria, 521, 112662.",
    
    r"Boublia, A., Lemaoui, T., Almustafa, G., Darwish, A. S., Benguerba, Y., Banat, F., & AlNashef, I. M. (2023). Critical Properties of Ternary Deep Eutectic Solvents Using Group Contribution with Extended Lee-Kesler Mixing Rules. ACS Omega, 8(14), 13177–13191.",
    
    r"Haghbakhsh, R., Bardool, R., Bakhtyari, A., Duarte, A. R. C., & Raeissi, S. (2019). Simple and global correlation for the densities of deep eutectic solvents. Journal of Molecular Liquids, 296, 111830.",

    r"Haghbakhsh, R., Taherzadeh, M., Duarte, A. R. C., & Raeissi, S. (2020). A general model for the surface tensions of deep eutectic solvents. Journal of Molecular Liquids, 307, 112972.",

    r"Peyrovedin, H., Haghbakhsh, R., Duarte, A. R. C., & Raeissi, S. (2020). A Global Model for the Estimation of Speeds of Sound in Deep Eutectic Solvents. Molecules 2020, Vol. 25, Page 1626, 25(7), 1626.",

    r"Taherzadeh, M., Haghbakhsh, R., Duarte, A. R. C., & Raeissi, S. (2020a). Estimation of the heat capacities of deep eutectic solvents. Journal of Molecular Liquids, 307, 112940.",

    r"Taherzadeh, M., Haghbakhsh, R., Duarte, A. R. C., & Raeissi, S. (2020b). Generalized Model to Estimate the Refractive Indices of Deep Eutectic Solvents. Journal of Chemical and Engineering Data, 65(8), 3965–3976.",

    r"Valderrama, J. O., Forero, L. A., & Rojas, R. E. (2012). Critical properties and normal boiling temperature of ionic liquids. Update and a new consistency test. Industrial and Engineering Chemistry Research, 51(22), 7838–7844.",

    r"Valderrama, J. O., Forero, L. A., & Rojas, R. E. (2019). Critical Properties of Metal-Containing Ionic Liquids. Industrial and Engineering Chemistry Research, 58(17), 7332–7340.",

    r"Valderrama, J. O., & Robles, P. A. (2007). Critical properties, normal boiling temperatures, and acentric factors of fifty ionic liquids. Industrial and Engineering Chemistry Research, 46(4), 1338–1344.",

    r"Valderrama, J. O., Sanga, W. W., & Lazzús, J. A. (2008). Critical properties, normal boiling temperature, and acentric factor of another 200 ionic liquids. Industrial and Engineering Chemistry Research, 47(4), 1318–1330.",
    ]

df_references = pd.DataFrame({
    "References" : referencias
})






