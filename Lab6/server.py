from paste.httpserver import serve
from jinja2 import Environment, FileSystemLoader
from pyramid.response import Response
from pyramid.config import Configurator

pages = {
  "/index.html": "/index.html",
  "/": "/index.html",
  "/about/aboutme.html": "/about/aboutme.html"
}

routes = {
    'index': '/index.html',
    'main': '/',
    'about': '/about/aboutme.html'
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

def render(request):
    template = environment.get_template(pages[request.current_route_path()]).render(css = css, js = js)
    return Response(template.encode())

config = Configurator()

for route in routes:
    config.add_route(route, routes[route])
    config.add_view(render, route_name = route)

app = config.make_wsgi_app()

serve(app, host = 'localhost', port = 80)