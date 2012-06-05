#!/usr/bin/env python
# -*- coding: utf8 -*-


import tornado.auth
import tornado.escape

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os
import time,datetime
import random


from tornado.options import define, options

class tab():
    def __init__(self,title,lists):
        self.title=title
        self.playlist=lists



def handle(str):
  try:
      return unicode(str,"gbk")
  except:
      return str
    

define("port", default=9999, help="run on the given port", type=int)
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/myspace", MyspaceHandler),
            (r"/login", LoginHandler),
            (r"/logout", LogoutHandler),

        ]
        settings = dict(
            cookie_secret="66oETzKXQAGaYdkL5gE%dJFuYh7EQnp2XdTP1o/Vo="%random.randint(1000,9999),
            login_url = "/login",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            # static_path=os.path.join(os.path.dirname(__file__), "static"),
            static_path=os.path.join(os.path.dirname(__file__), "statics"),
          #  xsrf_cookies=False,
            autoescape=None,
            debug=True
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        self.music_path="F:/html5/music/"
        self.SESSION={}


        self.mainlist=self.scans()
    
    def scans(self,userdir="",rootdir="F:/html5/music/"):
        rootdir+=userdir
        rootdir+="/"
        lists=os.listdir(rootdir)
        tablist=[i for i in lists if os.path.isdir(rootdir+i)]

        mainlist=[]
        for i in tablist:
            lists=os.listdir(rootdir+i)
            lists=[handle(l) for l in lists if l.endswith("mp3")]
            mainlist.append(tab(handle(i),lists))


        return mainlist



class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("mc_user")

class LoginHandler(BaseHandler, tornado.auth.GoogleMixin):
    def get(self):
        self.render("login.html")

    def post(self):
        username=self.get_argument("name")
        if username in ["testuser0","testuser2"]:
            self.set_secure_cookie("mc_user",username)
            lists=app.scans(username,"F:/html5/sound/")
            app.SESSION[username]={"mainlist":lists or app.mainlist}
            self.redirect("/myspace")
        else:
            self.redirect("/")

        

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect("/login")

class MainHandler(BaseHandler):
    
    def get(self):
        mainlist=app.mainlist
        rooturl="http://chat.lzu.me:9000/"
        if "User-Agent" in self.request.headers:
             agent = self.request.headers["User-Agent"]
             if "Mozilla/5.0" in agent and "Firefox" not in agent:

                self.render("index.html",mainlist=mainlist,rooturl=rooturl)
             else:
                self.render("flash-index.html",mainlist=mainlist,rooturl=rooturl)

            # else:
                # self.render("flash-index.html",mainlist=mainlist)

class MyspaceHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        mainlist=app.SESSION[self.current_user]["mainlist"]
        rooturl="http://chat.lzu.me:9001/%s/"%self.current_user
        if "User-Agent" in self.request.headers:
            agent = self.request.headers["User-Agent"]
            if "Mozilla/5.0" in agent and "Firefox" not in agent:
                self.render("index.html",mainlist=mainlist,rooturl=rooturl)
            else:
                self.render("flash-index.html",mainlist=mainlist,rooturl=rooturl)


tornado.options.parse_command_line()
app = Application()
app.listen(options.port)
tornado.ioloop.IOLoop.instance().start()


