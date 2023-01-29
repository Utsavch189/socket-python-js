import asyncio
import websockets
import json
from cache import Cache
import socket

MEMORY=Cache(126)
HOST='127.0.0.1'
PORT=9999

async def send_msg(res):
    global MEMORY
    target=res['to']
    if(MEMORY.get(target)):
        socket=MEMORY.get(target)['socket']
        await socket.send(res['message'])

async def save_client(res):
    global MEMORY
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
    global HOST,PORT
    print(f"server is listening at {HOST}:{PORT}...")
    try:
        await websockets.serve(connection,HOST,PORT)
    except Exception as e:
        print(e)

def run():
    event_loop=asyncio.get_event_loop()
    event_loop.run_until_complete(start_server())
    event_loop.run_forever()

run()
