import json

async def auth(user: bool = False) -> bool or str:
    with open('json/log.json', 'r') as log_file:
        data = json.load(log_file)
    if data['state'] == "login" and user == True:
        return data['user']
    elif data['state'] == "logout" and user == True:
        return False
    elif data['state'] == "login" and user == False:
        return 'ascess'
    else:
        return False
    
 
