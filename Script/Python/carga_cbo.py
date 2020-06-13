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

DIM_CBO_FAMILIA = pd.read_csv('Dados/ESTRUTURA CBO/CBO2002 - Familia.csv', sep=';', encoding='cp1252')
DIM_CBO_GRANDE_GRUPO = pd.read_csv('Dados/ESTRUTURA CBO/CBO2002 - Grande Grupo.csv', sep=';', encoding='cp1252')
DIM_CBO_OCUPACAO = pd.read_csv('Dados/ESTRUTURA CBO/CBO2002 - Ocupacao.csv', sep=';', encoding='cp1252')
DIM_CBO_SINONIMO = pd.read_csv('Dados/ESTRUTURA CBO/CBO2002 - Sinonimo.csv', sep=';', encoding='cp1252')
DIM_CBO_SUBGRUPOPRINCIPAL = pd.read_csv('Dados/ESTRUTURA CBO/CBO2002 - SubGrupo Principal.csv', sep=';', encoding='cp1252')
DIM_CBO_SUBGRUPO = pd.read_csv('Dados/ESTRUTURA CBO/CBO2002 - SubGrupo.csv', sep=';', encoding='cp1252')
DIM_CBO_PERFILOCUPACIONAL = pd.read_csv('Dados/ESTRUTURA CBO/CBO2002 - PerfilOcupacional.csv', sep=';', encoding='cp1252', error_bad_lines=False)

##================================================================================
## Cria engine de carga
##================================================================================

engine = cria_engine()
 
##================================================================================
## Carrega na azure
##================================================================================

DIM_CBO_FAMILIA.to_sql('DIM_CBO_FAMILIA', schema='dbo', con = engine, index=False, if_exists='replace')
DIM_CBO_GRANDE_GRUPO.to_sql('DIM_CBO_GRANDE_GRUPO', schema='dbo', con = engine, index=False, if_exists='replace')
DIM_CBO_OCUPACAO.to_sql('DIM_CBO_OCUPACAO', schema='dbo', con = engine, index=False, if_exists='replace')
DIM_CBO_SINONIMO.to_sql('DIM_CBO_SINONIMO', schema='dbo', con = engine, index=False, if_exists='replace')
DIM_CBO_SUBGRUPOPRINCIPAL.to_sql('DIM_CBO_SUBGRUPOPRINCIPAL', schema='dbo', con = engine, index=False, if_exists='replace')
DIM_CBO_SUBGRUPO.to_sql('DIM_CBO_SUBGRUPO', schema='dbo', con = engine, index=False, if_exists='replace')
DIM_CBO_PERFILOCUPACIONAL.to_sql('DIM_CBO_PERFILOCUPACIONAL', schema='dbo', con = engine, index=False, if_exists='replace')

