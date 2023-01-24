import asyncio
import websockets

all_clients=[]


async def send_msg(msg,target):
    for c in all_clients:
        if(c==target):
            await c.send(msg)

async def new_connection(client_socket,path):
    print("new connection","connection address : ",client_socket)
    all_clients.append(client_socket)
    while True:
        try:
            new_msg=await client_socket.recv()
            print("from client : ",new_msg)
            await send_msg(new_msg,client_socket)
        except:
            continue

async def start_server():
    print("server is listening!")
    await websockets.serve(new_connection,"localhost","9999")


event_loop=asyncio.get_event_loop()
event_loop.run_until_complete(start_server())
event_loop.run_forever()