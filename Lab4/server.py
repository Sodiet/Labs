from webob import Request
from jinja2 import Environment, FileSystemLoader

pages = {
  "/index.html": "/index.html",
  "/": "/index.html",
  "/about/aboutme.html": "/about/aboutme.html"
}

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

css = []
js = []

for i in includes:
    if(i.split('.')[1] == 'css'):
        css.append(i)
    else:
        js.append(i)

environment = Environment(loader = FileSystemLoader('.'))

class WsgiTopBottomMiddleware(object):
    '''
    WSGI for HTML editing
    '''
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        response = self.app(environ, start_response).decode()  # bytes to str
        yield response.encode()  # str to bytes


def app(environ, start_response):
    '''
    WSGI for HTML document
    '''
    path = environ.get('PATH_INFO', '')
    template = environment.get_template(pages[path])

    response_code = '200 OK'
    response_type = ('Content-Type', 'text/HTML')
    start_response(response_code, [response_type])

    return (template.render(css = css, js = js)).encode()

# WSGI to Middleware
app = WsgiTopBottomMiddleware(app)

print(Request.blank('/about/aboutme.html').get_response(app))
