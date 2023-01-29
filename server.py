import asyncio
import websockets
import json
from cache import Cache
import socket

MEMORY=Cache(126)


async def send_msg(res):
    target=res['to']
    if(MEMORY.get(target)):
        socket=MEMORY.get(target)['socket']
        await socket.send(res['message'])

async def save_client(res):
    MEMORY.put(res['id'],res)

async def connection(client_socket,path):    
    while True:
        if(path=='/socket'):
            try:
                res=json.loads(await client_socket.recv())
                if(res['init']==1):
                    print("new connection...")
                    new_user=(res | {'socket':client_socket})
                    await save_client(new_user)
                    print("user saved")
                else:
                    await send_msg(res)
            except:
                continue
        else:
            return socket.error 

async def start_server():
    print("server is listening!")
    try:
        await websockets.serve(connection,"127.0.0.1",9999)
    except Exception as e:
        print(e)


event_loop=asyncio.get_event_loop()
event_loop.run_until_complete(start_server())
event_loop.run_forever()