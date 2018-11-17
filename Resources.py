import json
from flask import request
from flask_restful import Resource, reqparse
import requests
import logging
import db

class Summoners(Resource):

	def get(self, name):
		summoner = db.Summoners.getByName(name)
		return summoner, 200

	def post(self, name, record):
		response = db.Summoners.insert(summoner)
		return response, 200

class Game(Resource):

	def get(self, ID):
		game = db.Games.getById(ID)
		return game, 200

class Games(Resource):

	def get(self):
		game = db.Games.getActive()
		return game, 200

	def post(self):
		record = request.get_json()
		logging.debug(f"Games.post() request.get_json() returned: {record}")
		response = db.Games.insert(record)
		if response:
			return response, 200
		else:
			return "Failed to update database", 500

	def put(self):
		record = request.get_json()
		logging.debug(f"Games.put() request.get_json() returned: {record}")
		existingRecord = db.Games.getById(record["ID"])
		logging.debug(f"Games.put() db.Games.getById({record["ID"]} returned {existingRecord}")

		for key, value in existingRecord.items():
			if not record[key]:
				record[key] = value

		response = db.Games.update(record)
		if response:
			return response, 200
		else:
			return "Failed to update database", 500

class Team(Resource):

	def get(self, teamId):
		record = db.Teams.getById(teamId)
		logging.debug(f"Teams.put() db.Teams.getById({record["ID"]} returned {existingRecord}")
		if record:
			return record, 200
		else:
			return f"Could not find a team with ID {teamId}.", 404


	def put(self, teamId):
		record = request.get_json()
		logging.debug(f"Teams.put() request.get_json() returned: {record}")
		existingRecord = db.Teams.getById(teamId)
		logging.debug(f"Teams.put() db.Teams.getById({record["ID"]} returned {existingRecord}")

		for key, value in existingRecord.items():
			if not record[key]:
				record[key] = value

		response = db.Teams.update(record)
		if response:
			return response, 200
		else:
			return "Failed to update database", 500

class Teams(Resource):

	def post(self):
		record = request.get_json()
		logging.debug(f"Teams.post() request.get_json() returned: {record}")
		response = db.Teams.insert(record)
		if response:
			return response, 200
		else:
			return "Failed to update database", 500


class Test(Resource):

	def post(self):
		record = request.get_json()
		logging.debug(f"Test.post() --> request.get_json(): {record}")
		response = db.Games.insert(record)
		if response:
			return response, 200
		else:
			return "Test failed", 500

	def get(self):
		db.Summoners.create()
		db.Games.create()
		return "This worked!", 200