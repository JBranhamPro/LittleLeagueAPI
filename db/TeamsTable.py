import logging

class TeamsTable(object):
	"""docstring for TeamsTable"""
	def __init__(self, conn, cursor):
		super(TeamsTable, self).__init__()
		self.c = cursor
		self.conn = conn
		
	def create(self):
		with self.conn:
			self.c.execute("""CREATE TABLE teams (
						id text,
						name text,
						player1 int,
						player2 int,
						player3 int,
						player4 int,
						player5 int,
						top int,
						jng int,
						mid int,
						adc int,
						sup int,
						value real,
						game text
						)""")

	def getById(self, ID):
		self.c.execute("SELECT * FROM teams WHERE id=:ID", {"ID":ID})
		records = self.c.fetchall()
		try:
			logging.debug(f"TeamsTable.getById({ID}) returned the following records: {records}")
			return records[0]
		except:
			logging.error(f"TeamsTable.getById({ID}) returned no records.")
			return None

	def getByGame(self, game):
		self.c.execute("SELECT * FROM teams WHERE game=:game", {"game":game})
		records = self.c.fetchall()
		try:
			logging.debug(f"TeamsTable.getByGame({game}) returned the following records: {records}")
			return records
		except:
			logging.error(f"TeamsTable.getByGame({game}) returned: {records}.")
			return None

	def insert(self, record):
		r = record

		try:
			existingRecord = self.getById(r["ID"])
			if existingRecord:
				logging.warning(f"TeamsTable.insert({r}) --> A record with id: {r['ID']} already exists. Insert aborted.")
				return
		except:
			# The "id" field is created in the insert method to ensure that no ID is duplicated... EVER. We NEVER want the user to be capable of determing ID's.
			# Other "null" fields are handled on the client side because we want to ensure that bad fields never make it to the table.
			r["ID"] = self.newId()
	
		with self.conn:
			self.c.execute("INSERT INTO teams VALUES (:id, :name, :player1, :player2, :player3, :player4, :player5, :top, :jng, :mid, :adc, :sup, :value, :game)", 
				{"id":r["ID"], "name":r["name"], "player1":r["player1"], "player2":r["player2"], "player3":r["player3"], "player4":r["player4"], "player5":r["player5"],
				"top":r["top"], "jng":r["jng"], "mid":r["mid"], "adc":r["adc"], "sup":r["sup"], "value":r["value"], "game":r["game"]})
			return f"TeamsTable.insert({r}) inserting new values into teams table"

	def newId(self):
		self.c.execute("SELECT id FROM teams ORDER BY id DESC LIMIT 1")
		latestId = self.c.fetchall()
		if not len(latestId): return 'T0001'
		latestId = latestId[0][0]
		logging.debug(f"TeamsTable.newId() fetched latest ID as : {latestId}")
		newId = int(latestId[1:]) + 1
		newId = str(newId).zfill(4)
		newId = 'T' + newId
		logging.debug(f"TeamsTable.newId() created new ID : {newId}")
		return newId

	def update(self, record):
		# updateString = f'UPDATE teams SET {record["attr"]} = {record["newValue"]} WHERE id = {record["ID"]}'
		r = record
		with self.conn:
			self.c.execute("UPDATE teams SET name = :name, player1 = :player1, player2 = :player2, player3 = :player3, player4 = :player4, player5 = :player5, top = :top, jng = :jng, mid = :mid, adc = :adc, sup = :sup) WHERE id = :id", 
				{"id":r["ID"], "name":r["name"], "player1":r["player1"], "player2":r["player2"], "player3":r["player3"], "player4":r["player4"], "player5":r["player5"],
				"top":r["top"], "jng":r["jng"], "mid":r["mid"], "adc":r["adc"], "sup":r["sup"], "value":r["value"], "game":r["game"]})