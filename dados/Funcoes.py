import pandas as pd
import numpy as np
import os

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

        Mdes = df_component['Mw (g/mol)'][0]
        
        Vcdes = df_component['Vc (mL/mol)'][0]

        Tcdes = df_component['Tc (K)'][0]

        Wdes = df_component['ω'][0]

        Pcdes = df_component['Pc (bar)'][0]

    
    else:
        df_component = df[df['Abr.'] == '/']

        Mdes = df_component['Mw (g/mol)'][0]

        Vcdes = df_component['Vc (mL/mol)'][0]

        Tcdes = df_component['Tc (K)'][0]

        Wdes = df_component['ω'][0]

        Pcdes = df_component['Pc (bar)'][0]


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




