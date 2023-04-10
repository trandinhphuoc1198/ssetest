import socket,time,os

s = socket.socket()
s.bind(('0.0.0.0',8080))
s.listen(100)
while True:
    conn,add= s.accept()
    conn.send(b"""HTTP/1.0 200 OK\r\nContent-Type: text/event-stream\r\nX-Accel-Buffering: no\r\n\r\n""")
    print(f'Connection established from  {str(add[0])}:{str(add[1])}')
    conn.send(b"data: connection OK\n\n")
    n=0
    success = 0
    while n<30:
        time.sleep(1)
        conn.send(f'data: {n} time\n\n'.encode('utf-8'))
        if os.path.exists('./yourkaiinID.jpg'):
            success = 1
            break
        n+=1
    if success:
        conn.send(b"event: check-image\n")
        conn.send(b'data: {"result": 1}\n\n')
    else:
        conn.send(b"event: check-image\n")
        conn.send(b'data: {"result": 0}\n\n')
    conn.close()