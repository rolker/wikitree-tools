#!/usr/bin/env python

import urllib2
import urllib
import cookielib
import getpass
import datetime
import os
import time
import json
import httplib

class WikiTreeError(Exception):
    pass

class LoginError(WikiTreeError):
    def __init__(self, msg):
        self.msg = msg

def loginPrompt(email = ''):
    print 'WikiTree Login'
    email_in = raw_input('Email ['+email+']:')
    if len(email_in):
        email = email_in
    return email, getpass.getpass()

class Profile:
    def __init__(self, id):
        self.id = id

    def fetch(self,connection):
        self.data = json.load(connection.getPage('action=getPerson&key='+self.id))
        return True

class Connection:
    def __init__(self, cookie_path=None, debug=False, login_prompt=loginPrompt):
        self.baseurl = 'http://apps.wikitree.com/api.php?'
        self.debug = debug
        self.login_prompt = login_prompt

        if cookie_path is None:
            cookie_path = os.path.expanduser('~/.wikitree/cookies.txt')
        self.jar = cookielib.MozillaCookieJar(cookie_path)
        try:
            self.jar.load()
        except IOError:
            if self.debug:
                print 'no cookies loaded'
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.jar))
        self.getUserInfo()

    def getPage(self,link):
        req = self.baseurl+link
        if self.debug:
            print 'req:',req
        try:
          ret = self.opener.open(req)
          if self.debug:
            print 'code:',ret.getcode()
            print 'info:',ret.info()
          return ret
        except (IOError, httplib.HTTPException):
          return None

    def login(self, max_tries=3):
        tries = 0
        email = ''
        while tries < max_tries:
            email,pwd = self.login_prompt(email)
            if self.debug:
                print 'email:',email,'password:','*'*len(pwd)
                
            req = self.baseurl+"action=login&email={email}&password={pwd}".format(email=email,pwd=pwd)
            ret = self.opener.open(req)
            
            if self.debug:
                print 'code:',ret.getcode()
                print 'info:',ret.info()

            if ret.getcode() == 200:
                cookie_dir = os.path.dirname(self.jar.filename)
                if not os.path.exists(cookie_dir):
                    os.makedirs(cookie_dir)
                self.jar.save()
                return
            tries += 1
        raise LoginError("Login failed")

    def getUserInfo(self, response=None):
        self.uid = None
        self.uname = None
        for c in self.jar:
            if c.name == 'wikidb_wtb_UserName':
                self.uname = c.value
            if c.name == 'wikidb_wtb_UserID':
                self.uid = c.value
        if self.uname is None:
            self.login()

if __name__ == '__main__':
    wt = Connection(debug=True)
    p = Profile(wt.uname)
    p.fetch(wt)
    print p.data
    #print json.load(wt.getPage('action=getPerson&key='+wt.uname))
        