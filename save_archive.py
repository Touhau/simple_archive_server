import json
import tarfile
import asyncio
import os

import requests

# Функция первой ручки:
# 1. Скачивает архив
# 2. Создаёт архив на устройстве
# 3. Разархивирует

async def save_archive(url: str, ID: int):
    await storage_change(ID, 'status', 'downloading')
    res = requests.get(url)

    await storage_change(ID, 'status', 'creating_archive')
    if os.path.isdir('data'):
        os.mkdir(f'data/{ID}')
    else:
        os.mkdir('data')
        os.mkdir(f'data/{ID}')
    with open(f'data/{ID}/{ID}.tar.gz', 'wb') as file:
        file.write(res.content)

    await storage_change(ID, 'status', 'unpacking')
    await storage_change(ID, 'path', os.path.abspath(f'data/{ID}/{ID}.tar.gz'))

    unpack_folder_name = str(ID) + '_files'
    os.mkdir(f'data/{ID}/{unpack_folder_name}')
    
    with tarfile.open(f'data/{ID}/{ID}.tar.gz') as archive:
        await storage_change(ID, 'files', archive.getnames())
        await storage_change(ID, 'total_files', len(archive.getnames()))
        archive.extractall(path = f'data/{ID}/{unpack_folder_name}')
    await storage_change(ID, 'status', 'ok')


# Запись в json
async def storage_change(ID: int, where_change: str, new_data: str):
    with open('json/storage.json', 'r') as data_file:
        data = json.load(data_file)
        data[ID][where_change] = new_data
    with open('json/storage.json', 'w') as write_data:
        json.dump(data, write_data, indent=4)



# def save_archive(url: str, ID: int):
#     storage_change(ID, 'status', 'downloading')
#     res = requests.get(url)

#     storage_change(ID, 'status', 'creating_archive')
#     os.mkdir(f'data/{ID}')
#     with open(f'data/{ID}/{ID}.tar.gz', 'wb') as file:
#         file.write(res.content)

#     storage_change(ID, 'status', 'unpacking')
#     storage_change(ID, 'path', os.path.abspath(f'data/{ID}/{ID}.tar.gz'))
#     unpack_folder_name = str(ID) + '_files'
#     os.mkdir(f'data/{ID}/{unpack_folder_name}')
#     with tarfile.open(f'data/{ID}/{ID}.tar.gz') as archive:
#         storage_change(ID, 'files', archive.getnames())
#         storage_change(ID, 'total_files', len(archive.getnames()))
#         archive.extractall(path = f'data/{ID}/{unpack_folder_name}')
#     storage_change(ID, 'status', 'ok')


# # Запись в json
# def storage_change(ID: int, where_change: str, new_data: str):
#     with open('json/storage.json', 'r') as data_file:
#         data = json.load(data_file)
#         data[ID][where_change] = new_data
#     with open('json/storage.json', 'w') as write_data:
#         json.dump(data, write_data, indent=4)