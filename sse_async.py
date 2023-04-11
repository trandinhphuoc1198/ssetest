import asyncio,socket,queue,os

async def server(clients,loop):
    server = socket.socket()
    server.bind(('0.0.0.0',8081))
    server.listen(10)
    server.setblocking(False)
    
    while True:
        client,address = await loop.sock_accept(server)
        print(f'Connected with {address}')
        clients.put(client)

async def handle_client(clients,loop):
    while True:
        await asyncio.sleep(0.5)
        if not clients.empty():
            try:
                client = clients.get()
                request = await loop.sock_recv(client,1000)
                id = request.decode('utf-8').split(' ')[1].split('?')[1].split('=')[1]
                await loop.sock_sendall(client,b"""HTTP/1.0 200 OK\r\nContent-Type: text/event-stream\r\nX-Accel-Buffering: no\r\n\r\n""")
                await loop.sock_sendall(client,b"data: Connection OK\n\n")
                
                n=0
                success = 0
                while n<20:
                    await asyncio.sleep(1)
                    await loop.sock_sendall(client,f'data: {n} time\n\n'.encode('utf-8'))
                    if os.path.exists(f'{id}'):
                        success = 1
                        break
                    n+=1
                    
                await loop.sock_sendall(client,b'event: check-image\ndata: {"result": 1}\n\n') if success else \
                await loop.sock_sendall(client,b'event: check-image\ndata: {"result": 0}\n\n')
                client.close()
            except:
                pass




async def main():
    loop = asyncio.get_event_loop()
    clients = queue.Queue()
    await asyncio.gather(*(handle_client(clients,loop) for _ in range(10)),server(clients,loop))

asyncio.run(main())
