#!/usr/bin/env python2
#-*- coding: utf-8 -*-

class RenrenClient(object):
  """Client of Renren  Account
  """

  user = None
  pwd = None

  def __init__(self, user, pwd):
    self.user = user
    self.pwd = pwd

  def _login(self):
    pass


def test():
  try:
    with open('user_pwd') as fi:
      user = fi.readline()
      pwd = fi.readline().decode('base64')
  except IOError:
    print 'Please add your username and pwd in ./user_pwd'
    exit(1)
  rclient = RenrenClient(user, pwd)

if __name__ == '__main__':
  test()
