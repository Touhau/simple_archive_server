import json
import asyncio
import re

import requests
from aiohttp import web
import aiohttp

from save_archive import save_archive
from auth import auth
from get_status import get_status
from delete_archive import delete_archive

async def log_in(request) -> web.Response:
    state = False
    data = await request.json()
    login = data['login']
    password = data['password']
    with open('json/auth.json', 'r') as auth_json:
        for user in json.load(auth_json):
            if login == user['login'] and password == user['password']:
                state = True
        if state == True:
            with open('json/log.json', 'r') as log_file:
                data = json.load(log_file)
                data['state'] = "login"
                data['user'] = login
            with open('json/log.json', 'w') as write_data:
                json.dump(data, write_data, indent=4)
            return web.Response(text='success auth')
        else:
            return web.Response(text='auth failed')


async def get_archive(request) -> web.Response or web.json_response:
    data = await request.text()
    url = re.search('http[s]?.+.gz', data).group(0)
    operation_ascess = await auth(True)
    if type(operation_ascess) == str:
        with open('json/storage.json', 'r') as read_storage:
            data_from_json = json.load(read_storage)
            task_id = len(data_from_json)
        json_data = {
            "id": task_id,
            "status": "",
            "files": [],
            "total_files": "",
            "path": "",
            "user": operation_ascess
        }
        data_from_json.append(json_data)
        with open('json/storage.json', 'w') as write_storage:
            json.dump(data_from_json, write_storage, indent=4)
        resp_data = {"task_id": task_id}
        await save_archive(url, task_id)
        # await asyncio.gather(asyncio.to_thread(save_archive, url, task_id))
        return web.json_response(resp_data)
    else:
        return web.Response(text = 'Auth error')

async def clear_log(request) -> web.Response:
    with open('json/log.json', 'r') as log_file:
        data = json.load(log_file)
        data['state'] = "logout"
        data['user'] = ''
    with open('json/log.json', 'w') as write_data:
        json.dump(data, write_data, indent=4)
    return web.Response(text='Success logout')


async def main() -> web.Application:
    await clear_log('')
    app = web.Application()
    app.add_routes([web.post('/archive', get_archive), 
                    web.get('/archive/{id}', get_status),
                    web.post('/auth', log_in),
                    web.get('/logout', clear_log),
                    web.delete('/archive/{id}', delete_archive)])
    return app


if __name__ == "__main__":
    web.run_app(main())
    
  
