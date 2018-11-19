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
		games = db.Games.getActive()

		activeGames = []

		for game in games:
			game = db.Games.convertToDict(game)
			activeGames.append(game)

		response = { "activeGames" : activeGames }

		return response, 200

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
		logging.debug(f"Games.put() db.Games.getById({record['ID']} returned {existingRecord}")

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
		logging.debug(f"Teams.put() db.Teams.getById({record['ID']} returned {record}")
		if record:
			return record, 200
		else:
			return f"Could not find a team with ID {teamId}.", 404


	def put(self, teamId):
		record = request.get_json()
		logging.debug(f"Teams.put() request.get_json() returned: {record}")
		existingRecord = db.Teams.getById(teamId)
		logging.debug(f"Teams.put() db.Teams.getById({record['ID']} returned {existingRecord}")

		for key, value in existingRecord.items():
			if not record[key]:
				record[key] = value

		response = db.Teams.update(record)
		if response:
			return response, 200
		else:
			return "Failed to update database", 500

class Teams(Resource):

	# def get(self):
	# 	activeTeams = []

	# 	activeGames = db.Games.getActive()
	# 	logging.debug(f"Teams.get() called db.Games.getActive() and returned: {activeGames}")
	# 	for game in activeGames["activeGames"]:
			
	# 		teamA = db.Teams.getById(game["teamA"])
	# 		if teamA:
	# 			logging.debug(f"Teams.get() called db.Teams.getById({game['teamA']}) and returned the following record: {teamA}")
	# 			teamA = {
	# 				"ID" : teamA[0],
	# 				"name" : teamA[1],
	# 				"player1" : teamA[2],
	# 				"player2" : teamA[3],
	# 				"player3" : teamA[4],
	# 				"player4" : teamA[5],
	# 				"player5" : teamA[6],
	# 				"top" : teamA[7],
	# 				"jng" : teamA[8],
	# 				"mid" : teamA[9],
	# 				"adc" : teamA[10],
	# 				"sup" : teamA[11],
	# 				"value" : teamA[12],
	# 				"game" : teamA[13]
	# 			}
	# 			activeTeams.append(teamA)

	# 		teamB = db.Teams.getById(game["teamB"])
	# 		if teamB:
	# 			logging.debug(f"Teams.get() called db.Teams.getById({game['teamB']}) and returned the following record: {teamB}")
	# 			teamB = {
	# 				"ID" : teamB[0],
	# 				"name" : teamB[1],
	# 				"player1" : teamB[2],
	# 				"player2" : teamB[3],
	# 				"player3" : teamB[4],
	# 				"player4" : teamB[5],
	# 				"player5" : teamB[6],
	# 				"top" : teamB[7],
	# 				"jng" : teamB[8],
	# 				"mid" : teamB[9],
	# 				"adc" : teamB[10],
	# 				"sup" : teamB[11],
	# 				"value" : teamB[12],
	# 				"game" : teamB[13]
	# 			}
	# 			activeTeams.append(teamB)

	# 	response = { "activeTeams" : activeTeams }
	# 	return response, 200

	def get(self):
		activeTeams = []

		activeGames = db.Games.getActive()

		for game in activeGames:
			gameId = game[0]
			teams = db.Teams.getByGame(gameId)
			for team in teams:
				team = {
					"ID" : team[0],
					"name" : team[1],
					"player1" : team[2],
					"player2" : team[3],
					"player3" : team[4],
					"player4" : team[5],
					"player5" : team[6],
					"top" : team[7],
					"jng" : team[8],
					"mid" : team[9],
					"adc" : team[10],
					"sup" : team[11],
					"value" : team[12],
					"game" : team[13]
				}
				activeTeams.append(team)

		response = { "activeTeams" : activeTeams }
		return response, 200

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