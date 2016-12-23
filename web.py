from paste.httpserver import serve
from jinja2 import Environment, FileSystemLoader
import selector

status = '200 OK'
http_headers = [('Content-Type', 'text/html; charset=UTF-8')]
ABOUTME = """<a href="about/aboutme.html"> ABOUTME.html </a>"""
INDEX = """<a href="/index.html"> INDEX.html </a>"""


class Base(object):

    def __init__(self, environ, start_response, link, template):
        self.env = environ
        self.start_response = start_response
        self.teplates = Environment(loader = FileSystemLoader('templates'))
        self.template = template
        self.link = link

    def __iter__(self):
        self.start_response(status, http_headers)
        template = self.teplates.get_template(self.template)
        yield template.render(link = self.link)


class Index(Base):

    def __init__(self, environ, start_response):
        Base.__init__(self, environ, start_response, INDEX, "index.html")


class AboutMe(Base):

    def __init__(self, environ, start_responce):
        Base.__init__(self, environ, start_responce,
                      ABOUTME, "about/aboutme.html")


def init():
    disp = selector.Selector()
    disp.add("/index.html", GET=INDEX)
    disp.add("/about/aboutme.html", GET=ABOUTME)
    return disp


if __name__ == "__main__":
    app = init()
serve(app, host='localhost', port=8000)
