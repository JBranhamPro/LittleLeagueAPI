import logging

class GamesTable(object):
	"""docstring for GamesTable"""
	def __init__(self, conn, cursor):
		super(GamesTable, self).__init__()
		self.c = cursor
		self.conn = conn
		
	def create(self):
		with self.conn:
			self.c.execute("""CREATE TABLE games (
						id text,
						name text,
						startTime datetime,
						active boolean,
						teamA text,
						teamB text,
						draftType text,
						randomChamps int,
						randomLanes boolean
						)""")

	def convertToDict(self, record):
		active = True if record[3] else False
		randomLanes = True if record[8] else False
		record = {"id":record[0], "name":record[1], "startTime":record[2], "active":active, "teamA":record[4], "teamB":record[5], "draftType":record[6], "randomChamps":record[7], "randomLanes":randomLanes}
		return record

	def getActive(self):
		self.c.execute("SELECT * FROM games WHERE active=1")
		records = self.c.fetchall()
		# games = []

		# for record in records:
		# 	game = self.convertToDict(record)
		# 	games.append(game)

		# games = { "activeGames" : games }

		# try:
		# 	logging.debug(f"GamesTable.getActive() returned the following records: {records}")
		# 	return games
		# except:
		# 	logging.error(f"GamesTable.getActive() returned no records.")
		# 	return None
		logging.debug(f"GamesTable.getActive() returned the following records: {records}")
		return records

	def getById(self, ID):
		self.c.execute("SELECT * FROM games WHERE id=:ID", {"ID":ID})
		records = self.c.fetchall()
		try:
			logging.debug(f"GamesTable.getById({ID}) returned the following records: {records}")
			record = records[0]
			record = self.convertToDict(record)
			return record
		except:
			logging.error(f"GamesTable.getById({ID}) returned no records.")
			return None

	# def getByName(self, name):
	# 	self.c.execute("SELECT * FROM games WHERE name=:name", {"name":name})
	# 	records = self.c.fetchall()
	# 	try:
	# 		logging.debug(f"GamesTable.getByName({name}) returned the following records: {records}")
	# 		return records[0]
	# 	except:
	# 		logging.error(f"GamesTable.getByName({name}) returned no records.")
	# 		return None

	def insert(self, record):
		r = record

		try:
			existingRecord = self.getById(r["ID"])
			if existingRecord:
				logging.warning(f"GamesTable.insert({r}) --> A record with id: {r ['ID']} already exists. Insert aborted.")
				return
		except:
			# The "id" field is created in the insert method to ensure that no ID is duplicated... EVER. We NEVER want the user to be capable of determing ID's.
			# Other "null" fields are handled on the client side because we want to ensure that bad fields never make it to the table.
			r["ID"] = self.newId()
		
		with self.conn:
			self.c.execute("INSERT INTO games VALUES (:id, :name, :startTime, :active, :teamA, :teamB, :draftType, :randomChamps, :randomLanes)",
				{"id":r["ID"], "name":r["name"], "active":r["active"], "startTime":r["startTime"], "teamA":r["teamA"], "teamB":r["teamB"], "draftType":r["draftType"], "randomChamps":r["randomChamps"], "randomLanes":r["randomLanes"]})
			logging.info(f"GamesTable.insert({record}) inserting new values into games table")
			return f"GamesTable.insert({record}) inserting new values into games table"

	def newId(self):
		self.c.execute("SELECT id FROM games ORDER BY id DESC LIMIT 1")
		latestId = self.c.fetchall()
		if not len(latestId): return 'G0001'
		latestId = latestId[0][0]
		logging.debug(f"GamesTable.newId() fetched latest ID as : {latestId}")
		newId = int(latestId[1:]) + 1
		newId = str(newId).zfill(4)
		newId = 'G' + newId
		logging.debug(f"GamesTable.newId() created new ID : {newId}")
		return newId

	def update(self, record):
		updateString = f'UPDATE summoners SET {record["attr"]} = {record["newValue"]} WHERE id = {record["ID"]}'

		with self.conn:
			self.c.execute(updateString)
			logging.debug(f"GamesTable.update({record}) updated a record in the games table")
			return True