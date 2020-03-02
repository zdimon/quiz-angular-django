#! /usr/bin/env python
import os
import tornado.httpserver
import tornado.ioloop
import tornado.wsgi
import sys
import django.core.handlers.wsgi
from co.settings import BASE_DIR
from tornado import web
sys.path.append(BASE_DIR)
def main():
        os.environ['DJANGO_SETTINGS_MODULE'] = 'co.settings'
        application = django.core.handlers.wsgi.WSGIHandler()
        container = tornado.wsgi.WSGIContainer(application)
        http_server = tornado.httpserver.HTTPServer(container)
        http_server.listen(8888)
        tornado.ioloop.IOLoop.instance().start()
if __name__ == "__main__":
                main()
