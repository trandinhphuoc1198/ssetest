import os
import sys
from wsgiref.simple_server import make_server
import cgi
import base64
import qrcode

PORT = int(os.getenv("PORT") or "8081")


def app(environ, start_response):
    id=environ['QUERY_STRING'].split('=')[1]
    path = environ["PATH_INFO"]
    if path == "/step1":
        headers = [("Content-type", "image/png")]
        img = qrcode.make(f"https://192.168.88.49/sse/step2?{environ['QUERY_STRING']}")
        img.save(f"{id}.png")
        with open(f"{id}.png",'rb') as f:
            # headers.append(("Content-Length",f"{os.path.getsize('./yourkaiinID.png')}"))
            start_response('200 OK',headers)
            yield f.read()
    elif path == "/step2":
        if environ['REQUEST_METHOD'] == 'POST':
            with open(f'{id}','wb') as ff:
                form = cgi.FieldStorage(fp=environ['wsgi.input'],environ=environ)
                f = form['img'].file
                ff.write(f.read())
                start_response('200 OK',[('Content-type', 'text/plain')])
                return b'Return to PC!!'
        else:
            yield from step2(environ, start_response)
    elif path == "/step3":
        yield from step3(environ, start_response)
    else:
        yield from index(environ, start_response)


def index(environ, start_response):
    status = "200 OK"
    headers = [
        ("Content-type", "text/html; charset=utf-8")
    ]
    start_response(status, headers)
    with open('./step1.html','rb') as f:
        yield f.read()
    
def step2(environ, start_response):
    status = "200 OK"
    headers = [
        ("Content-type", "text/html; charset=utf-8")
    ]
    start_response(status, headers)
    with open('./step2.html','rb') as f:
        yield f.read()

def step3(environ, start_response):
    id=environ['QUERY_STRING'].split('=')[1]
    status = "200 OK"
    headers = [
        ("Content-type", "text/html; charset=utf-8")
    ]
    with open(f'{id}','rb') as f:
        data = f.read()
    data_base64 = base64.b64encode(data)  # encode to base64 (bytes)
    data_base64 = data_base64.decode()
    start_response(status, headers)
    yield f"""
    <body>
    <h1>Your uploaded image</h1>
    <img src='data:image/png;base64,{data_base64}' width="400"  height="500">
    </body>
    """.encode('utf-8')

httpd = make_server("", PORT, app)
print(f"Serving on port {PORT}...", file=sys.stderr)

# Serve until process is killed
httpd.serve_forever()