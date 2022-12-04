import os
from pathlib import Path
from dotenv import load_dotenv

import tkinter as tk
from tkinter import filedialog

dotenv_path = Path('./envs/.maneger_infra.env')
load_dotenv(dotenv_path)

DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_NAME = os.getenv('DB_NAME')
CONTAINER_NAME = os.getenv('CONTAINER_NAME')

def validations():
    if (DB_USER == '' or DB_PASS == '' or DB_NAME == '' or CONTAINER_NAME is None):
        print(f'VERIFIQUE AS VAIÁVEIS DE AMBIENTE EM: {dotenv_path}')
        exit()

validations()

print('---------------')
print('|BANCO DE DADOS|')
print('---------------')
print('[1] - CRIAR DUMP\n[2] - RESTAURAR DUMP')
print('=========================================')

print('------')
print('|MINIO|')
print('------')
print('[3] - CRIAR USUÁRIO\n[4] - CRIAR BACKUP DO BUCKET\n[5] - RESTAURAR BACKUP DO BUCKET')
print('=========================================')

option = input('SELECIONE UMA DAS OPÇÕES: ')

#FUNÇÕES

# 1- CRIAR DUMP
def createDump():

    root = tk.Tk()
    root.withdraw()
    try:
        save_file_with_path = filedialog.asksaveasfile(defaultextension='.dump', title='Onde deseja salvar o DUMP?',) # Selecionando o diretório para salvar e nomear arquivo
        file_name_index = save_file_with_path.name.rfind('/') + 1                                                     # Extraindo o index inicial do nome (informado) do arquivo
        file_name = save_file_with_path.name[file_name_index:]                                                        # Extraindo o nome a partir do index
        path_file_index = file_name_index - 1                                                                         # Extraindo o index inicial do path (selecionado) do arquivo
        path = save_file_with_path.name[:path_file_index]                                                             # Extraindo o path a partir do index
        
        os.system(f"docker exec -it {CONTAINER_NAME} sh -c 'pg_dump -U {DB_USER} -d {DB_NAME} > /tmp/{file_name}'")   # Acessa o container e gera o arquivo DUMP
        os.system(f"docker cp {CONTAINER_NAME}:/tmp/{file_name} {path}")                                              # Copiando o arquivo para o path indicado 
    except:
        print('ERRO -> NECESSÁRIO NOMEAR O ARQUIVO!')

# 2- RESTAURANDO O DUMP
def restoreDump():

    try:
        open_file = filedialog.askopenfile()             # Selecionando o dump a ser restaurado
        file_name_index = open_file.name.rfind('/') + 1  # Extraindo o index inicial do nome (informado) do arquivo
        file_name = open_file.name[file_name_index:]     # Extraindo o nome a partir do index
        path_file_index = file_name_index - 1            # Extraindo o index inicial do path (selecionado) do arquivo
        path = open_file.name[:path_file_index]          # Extraindo o path a partir do index

        os.system(f"docker cp {path}/{file_name} {CONTAINER_NAME}:/tmp")                                                # Copiando oarquivo selecionado para o container
        os.system(f"docker exec -it {CONTAINER_NAME} psql -U {DB_USER} -c 'DROP DATABASE IF EXISTS {DB_NAME};'")        # 'Dropando' o banco de dados para 'zerá-lo'
        os.system(f"docker exec -it {CONTAINER_NAME} psql -U {DB_USER} -c 'CREATE DATABASE {DB_NAME};'")                # Recriando o banco de dados
        os.system(f"docker exec -it {CONTAINER_NAME} /bin/bash -c 'psql -U {DB_USER} -d {DB_NAME} < /tmp/{file_name}'") # Restaurando o arquivo (dump) enviado para o container

        print(f'\n\nBANCO: "{DB_NAME}"\nARQUIVO: "{file_name}"\nSTATUS: RESTAURANDO COM SUCESSO!')

    except:
        print('ERRO -> NECESSÁRIO SELECIONAR O ARQUIVO!')


match option:
    case '1':
        createDump()
    case '2':
        restoreDump()
    case '3':
        print('3')
    case '4':
        print('4')
    case '5':
        print('5')
    case _:
            print('OPÇÃO NÃO ENCONTRADA!')