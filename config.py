import base64
import os

repr = base64.b64decode(b'YjcxNDA0N2JiNWUxNjE6NzI1NTYxNGVAdXMtY2Rici1lYXN0LTAyLmNsZWFyZGIuY29tOjMzMDYvaGVyb2t1XzQzYmM1NmZmY2IxMWNhYQ==')
secret = repr.decode('utf-8')

DEBUG = False
HOST = '0.0.0.0'
PORT = os.environ.get("PORT", 5000)
SQLALCHEMY_DATABASE_URI = 'mysql://' + secret
#SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost:3306/garage_link_novo'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = 'YFUVMix#bgNV9AkEwsdb9@*!ZRkq@KfftK%CGQa*%4@bo!gevU'
