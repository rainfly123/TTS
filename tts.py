#!/usr/bin/env python
#coding:utf8
import daemon
import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import time
import uuid
import datetime
import mtts
import os
import json

from tornado.options import define, options
define("port", default=9280, help="run on the given port", type=int)

DNS="http://resource.qctchina.top"
PATH="/data/audio/"

class ttsHandler(tornado.web.RequestHandler):
    def get(self):
        text = self.get_argument("text")
        gender = self.get_argument("gender")
        self.set_header("Content-Type","audio/mpeg");
        data = mtts.GetTTS(gender, text)
        self.write(data)

class ttsurlHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header("Content-Type","application/json");
        text = self.get_argument("text")
        gender = self.get_argument("gender")
        data = mtts.GetTTS(gender, text)
        mylogo = str(uuid.uuid1()) + ".mp3"
        with open(os.path.join(PATH,mylogo), "wb") as f:
            f.write(data)
        val = {"code":0, "data": "http://120.76.190.105/" + mylogo, "message":"Ok"}
        self.write(json.dumps(val))


def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application([
            (r"/tts", ttsHandler),
            (r"/tts_url", ttsurlHandler),
        ],
        template_path = os.path.join(os.path.dirname(__file__), "templates"),
        static_path = os.path.join(os.path.dirname(__file__), "static"),
        debug = True,
        cookie_secret="xiechc@gmail.com",
        login_url="/login")

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
        daemon.daemonize("/tmp/tts.pid")
        main()
