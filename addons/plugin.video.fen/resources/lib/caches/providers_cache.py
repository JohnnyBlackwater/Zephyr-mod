# -*- coding: utf-8 -*-
import time
import datetime
import sqlite3 as database
from modules.kodi_utils import translate_path, confirm_dialog, path_exists
# from modules.kodi_utils import logger

SELECT_RESULTS = 'SELECT results, expires FROM results_data WHERE provider = ? AND db_type = ? AND tmdb_id = ? AND title = ? AND year = ? AND season = ? AND episode = ?'
DELETE_RESULTS = 'DELETE FROM results_data WHERE provider = ? AND db_type = ? AND tmdb_id = ? AND title = ? AND year = ? AND season = ? AND episode = ?'
INSERT_RESULTS = 'INSERT OR REPLACE INTO results_data VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
SINGLE_DELETE = 'DELETE FROM results_data WHERE db_type=? AND tmdb_id=?'
FULL_DELETE = 'DELETE FROM results_data'

database_path = translate_path('special://profile/addon_data/plugin.video.fen/providerscache.db')

class ExternalProvidersCache(object):
	def __init__(self):
		self.time = datetime.datetime.now()
		self.timeout = 240

	def get(self, source, db_type, tmdb_id, title, year, season, episode):
		result = None
		try:
			current_time = self._get_timestamp(self.time)
			dbcon = database.connect(database_path, timeout=self.timeout)
			dbcur = self._set_PRAGMAS(dbcon)
			dbcur.execute(SELECT_RESULTS, (source, db_type, tmdb_id, title, year, season, episode))
			cache_data = dbcur.fetchone()
			if cache_data:
				if cache_data[1] > current_time: result = eval(cache_data[0])
				else: self.delete(source, db_type, title, year, tmdb_id, season, episode, dbcon)
		except: pass
		return result

	def set(self, source, db_type, tmdb_id, title, year, season, episode, results, expire_time):
		try:
			expiration = datetime.timedelta(hours=expire_time)
			expires = self._get_timestamp(self.time + expiration)
			dbcon = database.connect(database_path, timeout=self.timeout)
			dbcur = self._set_PRAGMAS(dbcon)
			dbcur.execute(INSERT_RESULTS, (source, db_type, tmdb_id, title, year, season, episode, repr(results), int(expires)))
			dbcon.commit()
		except: pass

	def delete(self, source, db_type, tmdb_id, title, season, episode, dbcon=None):
		try:
			if not dbcon: dbcon = database.connect(database_path, timeout=self.timeout)
			dbcur = dbcon.cursor()
			dbcur.execute(DELETE_RESULTS, (source, db_type, tmdb_id, title, season, episode))
			dbcon.commit()
		except: return

	def _set_PRAGMAS(self, dbcon):
		dbcur = dbcon.cursor()
		dbcur.execute('''PRAGMA synchronous = OFF''')
		dbcur.execute('''PRAGMA journal_mode = OFF''')
		return dbcur

	def _get_timestamp(self, date_time):
		return int(time.mktime(date_time.timetuple()))

	def delete_cache(self, silent=False):
		try:
			if not path_exists(database_path): return 'failure'
			if not silent:
				if not confirm_dialog(): return 'cancelled'
			dbcon = database.connect(database_path)
			dbcur = self._set_PRAGMAS(dbcon)
			dbcur.execute(FULL_DELETE)
			dbcon.commit()
			dbcur.execute('VACUUM')
			dbcon.commit()
			dbcon.close()
			return 'success'
		except: return 'failure'

	def delete_cache_single(self, db_type, tmdb_id):
		try:
			if not path_exists(database_path): return False
			dbcon = database.connect(database_path)
			dbcur = self._set_PRAGMAS(dbcon)
			dbcur.execute(SINGLE_DELETE, (db_type, tmdb_id))
			dbcon.commit()
			dbcur.execute('VACUUM')
			dbcon.close()
			return True
		except: return False

providerCache = ExternalProvidersCache()
