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

# 2018
caged_201805 = pd.read_csv('Dados/CAGED/2018/CAGEDEST_052018.txt', sep=';', encoding='cp1252')
caged_201806 = pd.read_csv('Dados/CAGED/2018/CAGEDEST_062018.txt', sep=';', encoding='cp1252')
caged_201807 = pd.read_csv('Dados/CAGED/2018/CAGEDEST_072018.txt', sep=';', encoding='cp1252')
caged_201808 = pd.read_csv('Dados/CAGED/2018/CAGEDEST_082018.txt', sep=';', encoding='cp1252')
caged_201809 = pd.read_csv('Dados/CAGED/2018/CAGEDEST_092018.txt', sep=';', encoding='cp1252')
caged_201810 = pd.read_csv('Dados/CAGED/2018/CAGEDEST_102018.txt', sep=';', encoding='cp1252')
caged_201811 = pd.read_csv('Dados/CAGED/2018/CAGEDEST_112018.txt', sep=';', encoding='cp1252')
caged_201812 = pd.read_csv('Dados/CAGED/2018/CAGEDEST_122018.txt', sep=';', encoding='cp1252')

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


caged = caged_201805.append([caged_201806
                            ,caged_201807
                            ,caged_201808
                            ,caged_201809
                            ,caged_201810
                            ,caged_201811
                            ,caged_201812
                            ,caged_201901
                            ,caged_201902
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
## Puxa base para filtro de municípios do Sudeste (treinamento) e Sul (validação)
##================================================================================ 

# Puxa municipios  
municipio = pd.read_csv('Dados/CAGED/COD_MUNICIPIO_SUDESTE_E_SUL.csv', sep=';').drop_duplicates()

# renomeia coluna
municipio.columns = ['municipio']

# Transforma em string
municipio.municipio = municipio.municipio.astype(str)

# cria um set dos municípios
municipio = set(municipio.municipio)

##================================================================================
## Filtra os municípios
##================================================================================ 

caged_filtrado = caged_filtrado.loc[caged_filtrado['MUNICIPIO'].isin(municipio)]

##================================================================================
## Cria engine de carga
##================================================================================

engine = cria_engine()

##================================================================================
## Carrega na azure
##================================================================================

caged_filtrado.to_sql('STAGE_CAGED', schema='dbo', con = engine, index=False, if_exists='replace')
