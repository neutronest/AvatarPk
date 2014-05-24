#!/usr/bin/env python2
#-*- coding: utf-8 -*-

import requests
import logging
import json
import pickle
  
class RenrenClient(object):
  """Client of Renren  Account
  """

  user = None
  pwd = None
  session = None

  def __init__(self, user, pwd):
    self.user = user
    self.pwd = pwd
    self.session = requests.Session()

    if self._load_cookie():
      self._login()

    print self.session.get('http://www.renren.com/home', allow_redirects=False).content

  def _load_cookie(self):
    try:
      with open('./%s.cookie' % self.user, 'rb') as fi:
        self.session = pickle.load(fi)
        #cookie = pickle.load(fi)
        #self.session.cookies.update(cookie)
    except Exception as e:
      logging.info(e)
      return 1

  def _login(self):
    login_data = {
            'email': self.user,
            'password': self.pwd,
            'autoLogin': "true",
            'icode': '',
            'origURL': 'http://www.renren.com/home',
            'domain': 'renren.com',
            'key_id': '1',
            'captcha_type': 'web_login',
            }
    res = self.session.post('http://renren.com/ajaxLogin/login?1=1&uniqueTimestamp=201350118726', data=login_data)
    res_json = json.loads(res.content)

    url = res_json['homeUrl'] #回调url
    res = self.session.get(url)
    #print res.content
    print self.session.get('http://www.renren.com/home', allow_redirects=False).content

    with open('./%s.cookie' % self.user, 'wb') as fi:
      #cookie = requests.utils.dict_from_cookiejar(self.session.cookies)
      #pickle.dump(cookie, fi)
      pickle.dump(self.session, fi)


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
