from paste.httpserver import serve

CSS = '<link rel="stylesheet" href="/_static/%(name)s.css"/>\n'
JS = '<script src="/_static/%(name)s.js"></script>\n'

includes = [
    'app.js',
    'react.js',
    'leaflet.js',
    'D3.js',
    'moment.js',
    'math.js',
    'main.css',
    'bootstrap.css',
    'normalize.css',
]

pages = {
  "/index.html": "/index.html",
  "/": "/index.html",
  "/about/aboutme.html": "/about/aboutme.html"
}

class WsgiTopBottomMiddleware(object):
    '''
    WSGI for HTML editing
    '''
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        response = self.app(environ, start_response).decode()  # bytes to str

        cssStr = ''
        jsStr = ''

        for i in includes:
                if(i.split('.')[1] == 'css'):
                    cssStr += '<link rel="stylesheet" href="/_static/' + i + '"/>\n'
                else:
                    jsStr += '<script src="/_static/' + i + '"></script>\n'

        if response.find('</body>') > -1 and response.find('</head>') > -1:
          header, body = response.split('</head>')
          data, htmlend = body.split('</body>')

          yield (header + cssStr + '</head>' +
                 data + jsStr + '</body>' +
                 htmlend).encode()
        else:
          yield (cssStr + jsStr).encode()  # str to bytess


def app(environ, start_response):
    '''
    WSGI for HTML document
    '''
    path = environ.get('PATH_INFO', '')

    if path in pages:
      file = open('.' + pages[path], "rb")
      page = file.read()
      file.close()

      response_code = '200 OK'
      response_type = ('Content-Type', 'text/HTML')
      start_response(response_code, [response_type])

      return page
    else:
      response_code = '404 Not Found'
      response_type = ('Content-Type', 'text/HTML')
      start_response(response_code, [response_type])

      return '''
<!DOCTYPE html>
<html>
   <head>
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
      <title>404 Not Found</title>
   </head>
   <body>
   </body>
</html>
    '''.encode()

# WSGI to Middleware
app = WsgiTopBottomMiddleware(app)

# Start server
serve(app, host='localhost', port=80)

Результат:


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
<link rel="stylesheet" href="/_static/main.css"/>
<link rel="stylesheet" href="/_static/bootstrap.css"/>
<link rel="stylesheet" href="/_static/normalize.css"/>
</head>
<body>
    <a href="../index.html">Relative Path to index.html</a>
    <a href="https://github.com/Sodiet/Labs/blob/master/index.html">Absolute Path to index.html</a>
<script src="/_static/app.js"></script>
<script src="/_static/react.js"></script>
<script src="/_static/leaflet.js"></script>
<script src="/_static/D3.js"></script>
<script src="/_static/moment.js"></script>
<script src="/_static/math.js"></script>
</body>
</html>