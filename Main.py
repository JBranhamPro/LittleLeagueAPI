import logging
logging.basicConfig(filename='LittleLeagueApi.log', level=logging.DEBUG, format='%(asctime)s: %(levelname)s: %(module)s: \t%(message)s')
import socket
from flask import Flask
from flask_restful import Api, Resource, reqparse
from Resources import *

app = Flask(__name__)
api = Api(app)

api.add_resource(Game, "/games/<string:ID>/")
api.add_resource(Games, "/games/")
api.add_resource(Summoners, "/summoners/<string:name>/")
api.add_resource(Team, "/teams/<string:teamId>/")
api.add_resource(Teams, "/teams/")
api.add_resource(Test, "/test/")

host = socket.gethostbyname(socket.gethostname())
app.run(host=host, port=1919, debug=True)