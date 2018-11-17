import sqlite3
import logging
from .SummonersTable import SummonersTable
from .GamesTable import GamesTable

# conn = sqlite3.connect('LittleLeague.db')
conn = sqlite3.connect(':memory:', check_same_thread=False)
cursor = conn.cursor()

Summoners = SummonersTable(conn, cursor)
Games = GamesTable(conn, cursor)
Teams = TeamsTable(conn, cursor)

Summoners.create()
Games.create()