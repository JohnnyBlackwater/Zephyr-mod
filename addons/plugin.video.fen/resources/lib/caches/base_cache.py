# -*- coding: utf-8 -*-
import datetime
import time
import sqlite3 as database
from modules.kodi_utils import translate_path, window
# from modules.kodi_utils import logger

BASE_GET = 'SELECT expires, data FROM %s WHERE id = ?'
BASE_SET = 'INSERT OR REPLACE INTO %s(id, data, expires) VALUES (?, ?, ?)'
BASE_DELETE = 'DELETE FROM %s WHERE id = ?'

class BaseCache(object):
	def __init__(self, dbfile, table):
		self.dbfile = dbfile
		self.table = table
		self.time = datetime.datetime.now()
		self.timeout = 240

	def get(self, string):
		result = None
		try:
			current_time = self._get_timestamp(self.time)
			result = self.get_memory_cache(string, current_time)
			if result is None:
				dbcon = self.connect_database()
				dbcur = self.set_PRAGMAS(dbcon)
				dbcur.execute(BASE_GET % self.table, (string,))
				cache_data = dbcur.fetchone()
				if cache_data:
					if cache_data[0] > current_time:
						result = eval(cache_data[1])
						self.set_memory_cache(result, string, cache_data[1])
					else:
						self.delete(string, dbcon)
		except: pass
		return result

	def set(self, string, data, expiration=datetime.timedelta(days=30)):
		try:
			expires = self._get_timestamp(self.time + expiration)
			dbcon = self.connect_database()
			dbcur = self.set_PRAGMAS(dbcon)
			dbcur.execute(BASE_SET % self.table, (string, repr(data), int(expires)))
			dbcon.commit()
			self.set_memory_cache(data, string, int(expires))
		except: return None

	def get_memory_cache(self, string, current_time):
		result = None
		try:
			try: cachedata = window.getProperty(string.encode('utf-8'))
			except: cachedata = window.getProperty(string)
			if cachedata:
				cachedata = eval(cachedata)
				if cachedata[0] > current_time: result = cachedata[1]
		except: pass
		return result

	def set_memory_cache(self, data, string, expires):
		try:
			cachedata = (expires, data)
			try: cachedata_repr = repr(cachedata).encode('utf-8')
			except: cachedata_repr = repr(cachedata)
			window.setProperty(string, cachedata_repr)
		except: pass

	def delete(self, string, dbcon=None):
		try:
			if not dbcon: self.connect_database()
			dbcur = dbcon.cursor()
			dbcur.execute(BASE_DELETE % self.table, (string,))
			self.delete_memory_cache(string)
			dbcon.commit()
		except: pass

	def delete_memory_cache(self, string):
		window.clearProperty(string)

	def connect_database(self):
		return database.connect(self.dbfile, timeout=self.timeout)

	def set_PRAGMAS(self, dbcon):
		dbcur = dbcon.cursor()
		dbcur.execute('''PRAGMA synchronous = OFF''')
		dbcur.execute('''PRAGMA journal_mode = OFF''')
		return dbcur

	def _get_timestamp(self, date_time):
		return int(time.mktime(date_time.timetuple()))
