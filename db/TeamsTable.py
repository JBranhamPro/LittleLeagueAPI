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
						player1 int, #these fields hold the Riot Summoner ID
						player2 int,
						player3 int,
						player4 int,
						player5 int,
						top int, #same as player fields
						jng int,
						mid int,
						adc int,
						sup int,
						value real,
						game text #this field holds the ID for a game in the LittleLeague DB
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
			logging.error(f"TeamsTable.getByGame({game}) returned no records.")
			return None

	def insert(self, record):
		existingRecord = self.getById(record["ID"])
		if existingRecord:
			logging.warning(f"TeamsTable.insert({record}) --> A record with id: {record['ID']} already exists. Insert aborted.")
			return

		with self.conn:
			self.c.execute("INSERT INTO teams VALUES (:id, :name, :player1, :player2, :player3, :player4, :player5, :top, :jng, :mid, :adc, :sup)", 
				{"id":r["ID"], "name":r["name"], "player1":r["player1"], "player2":r["player2"], "player3":r["player3"], "player4":r["player4"], "player5":r["player5"],
				"top":r["top"], "jng":r["jng"], "mid":r["mid"], "adc":r["adc"], "sup":r["sup"], "value":r["value"], "game":r["game"]})

	def update(self, record):
		# updateString = f'UPDATE teams SET {record["attr"]} = {record["newValue"]} WHERE id = {record["ID"]}'
		with self.conn:
			self.c.execute("UPDATE teams SET name = :name, player1 = :player1, player2 = :player2, player3 = :player3, player4 = :player4, player5 = :player5, top = :top, jng = :jng, mid = :mid, adc = :adc, sup = :sup) WHERE id = :id", 
				{"id":r["ID"], "name":r["name"], "player1":r["player1"], "player2":r["player2"], "player3":r["player3"], "player4":r["player4"], "player5":r["player5"],
				"top":r["top"], "jng":r["jng"], "mid":r["mid"], "adc":r["adc"], "sup":r["sup"], "value":record.value, "game":r["game"]})