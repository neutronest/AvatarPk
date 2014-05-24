#!/usr/bin/env python2
#-*- coding: utf-8 -*-

import requests
import logging
import json
import pickle
import re

from random import random
  
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

    #print self.session.get('http://www.renren.com/home', allow_redirects=True).content

  def _load_cookie(self):
    try:
      with open('./%s.cookie' % self.user, 'rb') as fi:
        cookies = pickle.load(fi)
        self.session.cookies = cookies
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
      cookies = self.session.cookies
      pickle.dump(cookies, fi)

  def get(self, url):
    return self.session.get(url).content

  def post(self, url, data):
    return self.session.post(url, data=data).content

  def get_friend(self):
    url = 'http://rcd.renren.com/cwf_nget_newsfeed?t=%f' % random()
    data = {
        "uid": self.session.cookies.get('id'),
        "limit": "10000",
        "type": "WEB_FRIEND",
        "p": "0",
        "_rtk": "b7f8a4a",
        "requestToken": "1069452272",
        }
    return self.post(url, data)

  def get_visit_cnt(self, uid):
    content = self.get('http://www.renren.com/%s' % uid)
    try:
      return re.findall(r'最近来访 ([0-9]+)', content)[0]
    except:
      return re.findall(r'([0-9]+)</span>人看过', content)[0]

  def get_friend_cnt(self, uid):
    content = self.get('http://www.renren.com/%s' % uid)
    try:
      return re.findall(r'<span>([0-9]+)</span>&nbsp;好友', content)[0]
    except:
      return re.findall(r'class="count">\(([0-9]+)\)</a></div>', content)[0]

  
  def generate_post_form(self):
    s = '''
    uid:428400353
    limit:5
    type:WEB_FRIEND
    p:0
    _rtk:b7f8a4a
    requestToken:1069452272
    '''
    s = s.strip()
    print '{'
    for i in s.split('\n'):
      print '\t',
      print '"%s": "%s",' % tuple(i.strip().split(':'))
    print '}'

def test():
  try:
    with open('user_pwd') as fi:
      user = fi.readline()
      pwd = fi.readline()
      lens = len(pwd)
      lenx = lens - (lens % 4 if lens % 4 else 4)
      pwd = pwd[:lenx].decode('base64')
  except IOError:
    print 'Please add your username and pwd in ./user_pwd'
    exit(1)
  rclient = RenrenClient(user, pwd)
  print rclient.get_visit_cnt('428400353')
  print rclient.get_friend_cnt('428400353')
  print rclient.get_visit_cnt('738077255')
  print rclient.get_friend_cnt('738077255')

if __name__ == '__main__':
  test()
