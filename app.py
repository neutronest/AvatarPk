#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import inspect
import os

from tornado import web
from tornado import ioloop
from tornado import template
from tornado.web import  RequestHandler

ROOT = os.path.dirname(os.path.abspath(__file__))

loader = template.Loader('%s/templates' % ROOT)

class MainHandler(RequestHandler):

  def get(self):
    self.write(loader.load('index.html').generate())

class ApiHandler(RequestHandler):

  def get(self):
    self.write('Api')

class Api_TestHandler(RequestHandler):

  def get(self):
    self.write('Api/Test')


rules = [
    (r'/', MainHandler),
    (r'/static/(.*)', web.StaticFileHandler, {'path': '%s/static' % ROOT}),
    ]

for c in vars().keys():
  if c.endswith('Handler') and not c.startswith('Main') \
    and RequestHandler in inspect.getmro( vars()[c] )[1:]:
      rules.append( ('/%s' % '/'.join(c.rstrip('Handler').lower().split('_')), vars().get(c)) )
      rules.append( ('/%s/' % '/'.join(c.rstrip('Handler').lower().split('_')), vars().get(c)) )

app = web.Application(rules)

if __name__ == '__main__':
  app.listen(8888)
  ioloop.IOLoop.instance().start()
