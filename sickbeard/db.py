# Author: Nic Wolfe <nic@wolfeden.ca>
# URL: http://code.google.com/p/sickbeard/
#
# This file is part of Sick Beard.
#
# Sick Beard is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Sick Beard is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Sick Beard.  If not, see <http://www.gnu.org/licenses/>.



import os.path
import sqlite3

import sickbeard
from logging import *

from lib.tvdb_api import tvdb_api

class DBConnection:
		def __init__(self):
			self.connection = sqlite3.connect(os.path.join(sickbeard.PROG_DIR, "sickbeard.db"), 20)
			self.connection.row_factory = sqlite3.Row

		def action(self, query, args=None):
			
			self._checkDB()
			
			if query == None:
				return

			try:
				if args == None:
					self.connection.execute(query)
				else:
					self.connection.execute(query, args)
				self.connection.commit()
			except sqlite3.DatabaseError as e:
				Logger().log("Fatal error executing query: " + str(e), ERROR)
				raise
			

		def select(self, query, args=None):

			self._checkDB()
			sqlResults = []

			if query == None:
				Logger().log("Query must be a string (was None)", ERROR)
				return
			else:
				query = str(query)
		
			try:
				if args == None:
					Logger().log("SQL: "+query, DEBUG)
					sqlResults = self.connection.execute(query).fetchall()
				else:
					Logger().log("SQL: "+query+" with args "+str(args), DEBUG)
					sqlResults = self.connection.execute(query, args).fetchall()
			except sqlite3.DatabaseError as e:
				Logger().log("Fatal error executing query: " + str(e), ERROR)
				raise
			
			if sqlResults == None:
				return []
			
			return sqlResults
		
		def _checkDB(self):
			# Create the table if it's not already there
			try:
				sql = "CREATE TABLE tv_shows (show_id INTEGER PRIMARY KEY, location TEXT, show_name TEXT, tvdb_id NUMERIC, network TEXT, genre TEXT, runtime NUMERIC, quality NUMERIC, airs TEXT, status TEXT, seasonfolders NUMERIC, paused NUMERIC);"
				self.connection.execute(sql)
				self.connection.commit()
			except sqlite3.OperationalError as e:
				if str(e) != "table tv_shows already exists":
					raise

			# Create the table if it's not already there
			try:
				sql = "CREATE TABLE tv_episodes (episode_id INTEGER PRIMARY KEY, showid NUMERIC, tvdbid NUMERIC, name TEXT, season NUMERIC, episode NUMERIC, description TEXT, airdate NUMERIC, hasnfo NUMERIC, hastbn NUMERIC, status NUMERIC, location TEXT);"
				self.connection.execute(sql)
				self.connection.commit()
			except sqlite3.OperationalError as e:
				if str(e) != "table tv_episodes already exists":
					raise

			# Create the table if it's not already there
			try:
				sql = "CREATE TABLE info (last_backlog NUMERIC, last_tvdb NUMERIC);"
				self.connection.execute(sql)
				self.connection.commit()
			except sqlite3.OperationalError as e:
				if str(e) != "table info already exists":
					raise

			# Create the table if it's not already there
			try:
				sql = "CREATE TABLE history (action NUMERIC, date NUMERIC, showid NUMERIC, season NUMERIC, episode NUMERIC, quality NUMERIC, resource TEXT, provider NUMERIC);"
				self.connection.execute(sql)
				self.connection.commit()
			except sqlite3.OperationalError as e:
				if str(e) != "table history already exists":
					raise

