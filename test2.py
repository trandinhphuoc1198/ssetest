import socket,time,os

s = socket.socket()
s.bind(('0.0.0.0',8082))
s.listen(10)
while True:
    try:
        conn,add= s.accept()
        print(f'Proxied by nginx {str(add[0])}:{str(add[1])}')
        request = conn.recv(1000).decode('utf-8').split(' ')[1]
        print(f'Requested path: {request}')
        id = request.split('?')[1].split('=')[1]
        print(f'UserID={id}')
        conn.send(b"HTTP/1.0 200 OK\r\nContent-Type: text/event-stream\r\nX-Accel-Buffering: no\r\n\r\n")
        conn.send(b"data: connection OK\n\n")
        n=0
        success = 0
        while n<30:
            time.sleep(1)
            conn.send(f'data: {n} time\n\n'.encode('utf-8'))
            if os.path.exists(f'./{id}'):
                success = 1
                break
            n+=1
        if success:
            conn.send(b"event: check-image\n")
            conn.send(b'data: {"result": 1}\n\n')
        else:
            conn.send(b"event: check-image\n")
            conn.send(b'data: {"result": 0}\n\n')
        time.sleep(0.05)
        conn.close()
    except:
        pass
