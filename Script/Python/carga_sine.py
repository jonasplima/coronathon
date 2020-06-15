#!/usr/bin/python
#encoding: utf-8
# Carrega as biblioteca principal
import os as os
import pandas as pd
import numpy as np
import warnings  
from Script.Python.conecta_sql import validaUsereSenha
from Script.Python.conecta_sql import executaSQL_azure 
from Script.Python.conecta_sql import cria_engine
from sqlalchemy import create_engine 
import urllib
from prompt_toolkit import prompt

# Removendo warnings
warnings.simplefilter(action="ignore", category=PendingDeprecationWarning)
warnings.simplefilter(action='ignore', category=FutureWarning)

##================================================================================
## Carrega bases de CBO
##================================================================================

# SINE 
sinesp = pd.read_csv('Dados/SINE/D_ETL_IMO_EXTRACAO_SINE_ABERTO_TRABALHADORES_SP.csv', sep=';', encoding='latin_1') 

##================================================================================
## Concatena base da CAGED
##================================================================================

sine = sinesp

##================================================================================
## Filtra somente quem foi admitido 
##================================================================================ 
 
sine = sine[['DEFICIENCIAS', 'PRETENSOES', 'CODIGO_MUNICIPIO_IBGE', 'ESCOLARIDADE']]

##================================================================================
## Ajusta os tipos de variáveis
##================================================================================ 

sine['DEFICIENCIAS'] = sine['DEFICIENCIAS'].astype(str)
sine['PRETENSOES'] = sine['PRETENSOES'].astype(str)
sine['CODIGO_MUNICIPIO_IBGE'] = sine['CODIGO_MUNICIPIO_IBGE'].astype(str) 
sine['ESCOLARIDADE'] = sine['ESCOLARIDADE'].astype(str)

sine.loc[sine.DEFICIENCIAS == 'nan', ['DEFICIENCIAS']] = False
sine.loc[sine.DEFICIENCIAS != 'nan', ['DEFICIENCIAS']] = True

sine.loc[sine.ESCOLARIDADE == 'Médio Incompleto', ['ESCOLARIDADE']] = '6'
sine.loc[sine.ESCOLARIDADE == 'Médio Completo', ['ESCOLARIDADE']] = '7'
sine.loc[sine.ESCOLARIDADE == 'Fundamental Completo', ['ESCOLARIDADE']] = '5'
sine.loc[sine.ESCOLARIDADE == 'Superior Incompleto', ['ESCOLARIDADE']] = '8'
sine.loc[sine.ESCOLARIDADE == 'Analfabeto', ['ESCOLARIDADE']] = '1'
sine.loc[sine.ESCOLARIDADE == 'Não Identificado', ['ESCOLARIDADE']] = '-1'
sine.loc[sine.ESCOLARIDADE == 'Superior Completo', ['ESCOLARIDADE']] = '9'
sine.loc[sine.ESCOLARIDADE == 'Fundamental Incompleto', ['ESCOLARIDADE']] = '4'
sine.loc[sine.ESCOLARIDADE == 'Nenhum', ['ESCOLARIDADE']] = '-1'
sine.loc[sine.ESCOLARIDADE == 'Especialização', ['ESCOLARIDADE']] = '10'
sine.loc[sine.ESCOLARIDADE == 'Mestrado', ['ESCOLARIDADE']] = '10'
sine.loc[sine.ESCOLARIDADE == 'Doutorado', ['ESCOLARIDADE']] = '11'
sine.loc[sine.ESCOLARIDADE == 'N', ['ESCOLARIDADE']] = '-1' 

##================================================================================
## Separa amostra
##================================================================================ 

sine = sine.loc[(sine.PRETENSOES != 'nan')].head(30000)

##================================================================================
## Gera uma linha para cada CBO para análise
##================================================================================ 

sine_trabalhador = pd.DataFrame(columns=['DEFICIENCIAS', 'CODIGO_MUNICIPIO_IBGE', 'ESCOLARIDADE', 'CBO'])

for i in sine.index:
    print(i) 
    preten = list(sine.loc[sine.index == i, 'PRETENSOES'])[0]
    ttal = preten.count('|')
    lista_cbo = list()
    indice = 0
    lista_cbo.append(preten[indice:6])
    for x in range(0, ttal):
        indice = preten.find("|", indice+1)
        lista_cbo.append(preten[indice+1:indice+7])
    
    for z in lista_cbo:
        sine_trabalhador = sine_trabalhador.append(pd.DataFrame({   'DEFICIENCIAS':list(sine.loc[sine.index == i, 'DEFICIENCIAS']),
                                                                    'CODIGO_MUNICIPIO_IBGE':list(sine.loc[sine.index == i, 'CODIGO_MUNICIPIO_IBGE']), 
                                                                    'ESCOLARIDADE':list(sine.loc[sine.index == i, 'ESCOLARIDADE']),
                                                                    'CBO':z
                                                                }))

##================================================================================
## Gera arquivo 
##================================================================================

sine.to_csv('Dados/SINE/SINE.csv', sep=';', index=False)
 