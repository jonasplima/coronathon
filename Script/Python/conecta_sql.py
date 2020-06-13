def validaUsereSenha():
    from prompt_toolkit import prompt
    import pyodbc
    username = input('Digite o usuário de acesso ao Banco de dados para executar o script: \n-> ')
    password = prompt('\nDigite a senha de acesso ao Banco de dados para executar o script: \n-> ', is_password=True) 
    server = 'coronathon.database.windows.net' 
    database = 'coronathon'  
    try:
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
        print("Conectado! ")
        return username, password
    except:
        print("Erro de usuário e senha. Por favor, tente novamente! ")




def executaSQL_azure(script, username = None, password = None):
    import pyodbc 
    from prompt_toolkit import prompt
    import pandas as pd
    if (username == None) or (password == None) or (username == '') or (password == ''):
        username = input('Digite o usuário de acesso ao Banco de dados para executar o script: \n-> ')
        password = prompt('\nDigite a senha de acesso ao Banco de dados para executar o script: \n-> ', is_password=True) 
    else:
        pass
    
    server = 'coronathon.database.windows.net' 
    database = 'coronathon'  
    try:
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
        print("Conectado! \n")
        resultado = pd.read_sql_query(script, cnxn)
        cnxn.close()
        return resultado
    
    except:
        print("Erro de usuário e senha. Por favor, tente novamente! ")


