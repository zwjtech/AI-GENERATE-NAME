import tornado.web

class BaseHandler(tornado.web.RequestHandler):
 #blog.csdn.net/moshowgame 解决跨域问题
 def set_default_headers(self):
  self.set_header('Access-Control-Allow-Credentials', 'true')
  self.set_header('Access-Control-Allow-Origin', '*')
  self.set_header('Access-Control-Allow-Headers', '*')
  self.set_header('Access-Control-Max-Age', 10000)
  self.set_header('Content-type', 'application/json')
  self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
  self.set_header('Access-Control-Allow-Headers',#'*')
      'authorization, Authorization, Content-Type, Access-Control-Allow-Origin, Access-Control-Allow-Headers, X-Requested-By, Access-Control-Allow-Methods')
