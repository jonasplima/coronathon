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
## Carrega bases do CAGED
##================================================================================
 
# 2019
caged_201901 = pd.read_csv('Dados/CAGED/2019/CAGEDEST_012019.txt', sep=';', encoding='cp1252')
caged_201902 = pd.read_csv('Dados/CAGED/2019/CAGEDEST_022019.txt', sep=';', encoding='cp1252')
caged_201903 = pd.read_csv('Dados/CAGED/2019/CAGEDEST_032019.txt', sep=';', encoding='cp1252')
caged_201904 = pd.read_csv('Dados/CAGED/2019/CAGEDEST_042019.txt', sep=';', encoding='cp1252')
caged_201905 = pd.read_csv('Dados/CAGED/2019/CAGEDEST_052019.txt', sep=';', encoding='cp1252')
caged_201906 = pd.read_csv('Dados/CAGED/2019/CAGEDEST_062019.txt', sep=';', encoding='cp1252')
caged_201907 = pd.read_csv('Dados/CAGED/2019/CAGEDEST_072019.txt', sep=';', encoding='cp1252')
caged_201908 = pd.read_csv('Dados/CAGED/2019/CAGEDEST_082019.txt', sep=';', encoding='cp1252')
caged_201909 = pd.read_csv('Dados/CAGED/2019/CAGEDEST_092019.txt', sep=';', encoding='cp1252')
caged_201910 = pd.read_csv('Dados/CAGED/2019/CAGEDEST_102019.txt', sep=';', encoding='cp1252')
caged_201911 = pd.read_csv('Dados/CAGED/2019/CAGEDEST_112019.txt', sep=';', encoding='cp1252')
caged_201912 = pd.read_csv('Dados/CAGED/2019/CAGEDEST_122019.txt', sep=';', encoding='cp1252')

##================================================================================
## Concatena base da CAGED
##================================================================================

caged = caged_201901.append([caged_201902
                            ,caged_201903
                            ,caged_201904
                            ,caged_201905
                            ,caged_201906
                            ,caged_201907
                            ,caged_201908
                            ,caged_201909
                            ,caged_201910
                            ,caged_201911
                            ,caged_201912])

##================================================================================
## Filtra somente quem foi admitido 
##================================================================================ 
 
caged_filtrado = caged.loc[caged['Admitidos/Desligados'] == 1, ['CBO 2002 Ocupação', 'Grau Instrução', 'Município', 'Salário Mensal', 'Ind Portador Defic']]

##================================================================================
## Ajusta os tipos de variáveis
##================================================================================ 
  
caged_filtrado['CBO 2002 Ocupação'] = caged_filtrado['CBO 2002 Ocupação'].astype(str)
caged_filtrado['Grau Instrução'] = caged_filtrado['Grau Instrução'].astype(str)
caged_filtrado['Município'] = caged_filtrado['Município'].astype(str)
caged_filtrado['Salário Mensal'] = caged_filtrado['Salário Mensal'].map(lambda x: float(str(x).replace(',','.')))
caged_filtrado['Ind Portador Defic'] = caged_filtrado['Ind Portador Defic'].astype(bool)

##================================================================================
## Renomeia colunas
##================================================================================ 

caged_filtrado.rename(columns={'CBO 2002 Ocupação':'CBO', 'Grau Instrução':'GRAU_INSTRUCAO', 'Município':'MUNICIPIO', 'Salário Mensal':'SALARIO', 'Ind Portador Defic':'PORTADOR_DEFICIENCIA'}, inplace=True)
 
##================================================================================
## Filtra os municípios
##================================================================================ 
# Puxa municipios  
municipio = pd.read_csv('Dados/CAGED/CODIGO_MUNICIPIO_SUDESTE_E_SUL.csv', sep=';').drop_duplicates()

caged_filtrado = caged_filtrado.loc[caged_filtrado['MUNICIPIO'].isin(municipio.loc[municipio.ESTADO == 'SP', 'CODIGO'].astype(str))]


##================================================================================
## SEPARA AMOSTRA
##================================================================================ 

amostra = caged_filtrado[['CBO', 'PORTADOR_DEFICIENCIA']].groupby(['CBO']).count().sort_values(by='PORTADOR_DEFICIENCIA', ascending=False).reset_index()
amostra = amostra.head(30)

caged_filtrado = caged_filtrado.loc[caged_filtrado['CBO'].isin(amostra.CBO.unique())]

##================================================================================
## Cria engine de carga
##================================================================================

caged_filtrado.loc[caged_filtrado.GRAU_INSTRUCAO.isin(['2','3','4']), 'GRAU_INSTRUCAO'] = '4'
caged_filtrado.loc[caged_filtrado.GRAU_INSTRUCAO.isin(['11']), 'GRAU_INSTRUCAO'] = '10'

##================================================================================
## Gera arquivo 
##================================================================================

caged_filtrado.to_csv('Dados/CAGED/CAGED.csv', sep=';', index=False)