import logging

class SummonersTable(object):
	"""docstring for SummonersTable"""
	def __init__(self, conn, cursor):
		super(SummonersTable, self).__init__()
		self.c = cursor
		self.conn = conn
		
	def create(self):
		with self.conn:
			self.c.execute("""CREATE TABLE summoners (
						id int,
						name text,
						tier text,
						rank text,
						value real,
						primaryRole text,
						secondaryRole text,
						game text
						)""")

	def getById(self, ID):
		self.c.execute("SELECT * FROM summoners WHERE id=:ID", {"ID":ID})
		records = self.c.fetchall()
		try:
			logging.debug(f"SummonersTable.getById({ID}) returned the following records: {records}")
			return records[0]
		except:
			logging.error(f"SummonersTable.getById({ID}) returned no records.")
			return None

	def getByGame(self, game):
		self.c.execute("SELECT * FROM summoners WHERE game=:game", {"game":game})
		records = self.c.fetchall()
		try:
			logging.debug(f"SummonersTable.getByGame({game}) returned the following records: {records}")
			return records
		except:
			logging.error(f"SummonersTable.getByGame({game}) returned no records.")
			return None

	def getByName(self, name):
		self.c.execute("SELECT * FROM summoners WHERE name=:name", {"name":name})
		records = self.c.fetchall()
		try:
			logging.debug(f"SummonersTable.getByName({name}) returned the following records: {records}")
			return records[0]
		except:
			logging.error(f"SummonersTable.getByName({name}) returned no records.")
			return None

	def insert(self, record):
		summonerData = self.getById(record["ID"])
		if summonerData: 
			logging.warning(f"SummonersTable.insert({record}) --> A record with id: {record['ID']} already exists. Insert aborted.")
			return

		with self.conn:
			self.c.execute("INSERT INTO summoners VALUES (:id, :name, :tier, :rank, :value, :primaryRole, :secondaryRole, null)", 
				{"id":record.id, "name":record.name, "tier":record.tier, "rank":record.rank, "value":record.value, "primaryRole":record.primary, "secondaryRole":record.secondary})

	def update(self, record):
		updateString = f'UPDATE summoners SET {record["attr"]} = {record["newValue"]} WHERE id = {record["ID"]}'

		with self.conn:
			self.c.execute(updateString)