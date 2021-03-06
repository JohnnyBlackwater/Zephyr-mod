# -*- coding: utf-8 -*-
import requests
import re
import datetime
import base64
import json
import sqlite3 as database
try: from urllib import urlencode, quote # Python 2
except ImportError: from urllib.parse import urlencode, quote # Python 3
from caches.main_cache import main_cache
from modules.utils import to_utf8
from modules.settings_reader import get_setting, set_setting
# from modules.kodi_utils import logger

SORT = {'s1': 'relevance', 's1d': '-', 's2': 'dsize', 's2d': '-', 's3': 'dtime', 's3d': '-'}
SEARCH_PARAMS = {'st': 'adv', 'sb': 1, 'fex': 'm4v,3gp,mov,divx,xvid,wmv,avi,mpg,mpeg,mp4,mkv,avc,flv,webm', 'fty[]': 'VIDEO', 'spamf': 1, 'u': '1', 'gx': 1, 'pno': 1, 'sS': 3}
SEARCH_PARAMS.update(SORT)

def import_easynews():
	''' API version setting currently disabled '''
	# if get_setting('easynews.api_version') == '0':
	# 	return EasyNewsAPI()
	# else:
	# 	return EasyNewsAPIv3()
	return EasyNewsAPI()

class EasyNewsAPI:
	def __init__(self):
		self.base_url = 'https://members.easynews.com'
		self.search_link = '/2.0/search/solr-search/advanced'
		self.username = get_setting('easynews_user')
		self.password = get_setting('easynews_password')
		self.moderation = 1 if get_setting('easynews_moderation') == 'true' else 0
		self.auth = self._get_auth()
		self.account_link = 'https://account.easynews.com/editinfo.php'
		self.usage_link = 'https://account.easynews.com/usageview.php'
		self.timeout = 20.0
		self.base_get = self._get
		self.base_process = self._process_files
		self.base_resolver = self.resolver

	def _get_auth(self):
		try:
			auth = 'Basic ' + base64.b64encode('%s:%s' % (self.username, self.password))
		except:
			user_info = '%s:%s' % (self.username, self.password)
			user_info = user_info.encode('utf-8')
			auth = 'Basic ' + base64.b64encode(user_info).decode('utf-8')
		return auth

	def search(self, query):
		search_url, params = self._translate_search(query)
		cache_name = 'fen_EASYNEWS_SEARCH_' + urlencode(params)
		cache = main_cache.get(cache_name)
		if cache:
			files = cache
		else:
			results = self.base_get(search_url, params)
			files = to_utf8(self.base_process(results))
			main_cache.set(cache_name, files, expiration=datetime.timedelta(hours=48))
		return files

	def account(self):
		from modules.dom_parser import parseDOM
		try:
			account_html = self._get(self.account_link)
			if account_html == None or account_html == '': raise Exception()
			account_info = parseDOM(account_html, 'form', attrs={'id': 'accountForm'})
			account_info = parseDOM(account_info, 'td')[0:11][1::3]
			usage_html = self._get(self.usage_link)
			if usage_html == None or usage_html == '': raise Exception()
			usage_info = parseDOM(usage_html, 'div', attrs={'class': 'table-responsive'})
			usage_info = parseDOM(usage_info, 'td')[0:11][1::3]
			return account_info, usage_info
		except Exception:
			pass

	def _process_files(self, files):
		def _process():
			for item in files:
				try:
					valid_result = True
					post_hash, size, post_title, ext, duration = item['0'], item['4'], item['10'], item['11'], item['14']
					if 'alangs' in item and item['alangs']: language = item['alangs']
					else: language = ''
					if 'type' in item and item['type'].upper() != 'VIDEO': valid_result = False
					elif 'virus' in item and item['virus']: valid_result = False
					elif re.match(r'^\d+s', duration) or re.match(r'^[0-5]m', duration): valid_result = False
					if not valid_result: continue
					stream_url = down_url + quote('/%s/%s/%s%s/%s%s' % (dl_farm, dl_port, post_hash, ext, post_title, ext))
					file_dl = stream_url + '|Authorization=%s' % (quote(self.auth))
					result = {'name': post_title,
							  'size': size,
							  'rawSize': item['rawSize'],
							  'url_dl': file_dl,
							  'version': 'version2',
							  'full_item': item,
							  'language': language}
					yield result
				except Exception as e:
					from modules.kodi_utils import logger
					logger('FEN easynews API Exception', str(e))
		down_url = files.get('downURL')
		dl_farm = files.get('dlFarm')
		dl_port = files.get('dlPort')
		files = files.get('data', [])
		results = list(_process())
		return results

	def _process_files_v3(self, results):
		def _process():
			for item in files:
				try:
					valid_result = True
					post_hash, size, post_title, ext, duration, sig = item['hash'], item['bytes'], item['filename'], item['extension'], item['runtime'], item['sig']
					if 'alangs' in item and item['alangs']: language = item['alangs']
					else: language = ''
					if 'type' in item and item['type'].upper() != 'VIDEO': valid_result = False
					elif 'virus' in item and item['virus']: valid_result = False
					elif re.match(r'^\d+s', duration) or re.match(r'^[0-5]m', duration): valid_result = False
					if not valid_result: continue
					url_dl = self.stream_url % (post_hash, ext, post_title, sid, sig)
					result = {'name': post_title,
							  'size': size,
							  'rawSize': size,
							  'url_dl': url_dl,
							  'version': 'version3',
							  'full_item': item}
					yield result
				except Exception as e:
					from modules.kodi_utils import logger
					logger('FEN easynews API Exception', str(e))
		files = results.get('data', [])
		sid = results.get('sid')
		results = list(_process())
		return results

	def _translate_search(self, query):
		params = SEARCH_PARAMS
		params['pby'] = 350
		params['safeO'] = self.moderation
		params['gps'] = query
		url = self.base_url + self.search_link
		return url, params

	def _get(self, url, params={}):
		headers = {'Authorization': self.auth}
		response = requests.get(url, params=params, headers=headers, timeout=self.timeout).text
		try: return to_utf8(json.loads(response))
		except: return to_utf8(response)

	def _get_v3(self, url, params={}):
		headers = {'Authorization': self.auth}
		response = requests.get(url, params=params, headers=headers, timeout=self.timeout).content
		response = re.compile(self.regex,re.DOTALL).findall(response)[0]
		response = response + '}'
		try: return to_utf8(json.loads(response))
		except: return to_utf8(response)

	def resolve_easynews(self, url_dl):
		return self.base_resolver(url_dl)

	def resolver(self, url_dl):
		return url_dl

	def resolver_v3(self, url_dl):
		headers = {'Authorization': self.auth}
		response = requests.get(url_dl, headers=headers, stream=True, timeout=40.0)
		stream_url = response.url
		resolved_link = stream_url + '|Authorization=%s' % (quote(self.auth))
		return resolved_link

class EasyNewsAPIv3(EasyNewsAPI):
	def __init__(self):
		EasyNewsAPI.__init__(self)
		self.base_url = 'https://members-beta.easynews.com/3.0/index/basic'
		self.stream_url = 'https://members-beta.easynews.com/os/3.0/auto/443/%s%s/%s?sid=%s&sig=%s'
		self.search_link = ''
		self.regex='var INIT_RES = (.+?)};'
		self.base_get = self._get_v3
		self.base_process = self._process_files_v3
		self.base_resolver = self.resolver_v3

def clear_media_results_database():
	import os
	from modules.kodi_utils import translate_path, window
	EASYNEWS_DATABASE = translate_path('special://profile/addon_data/plugin.video.fen/maincache.db')
	dbcon = database.connect(EASYNEWS_DATABASE)
	dbcur = dbcon.cursor()
	dbcur.execute("SELECT id FROM maincache WHERE id LIKE 'fen_EASYNEWS_SEARCH_%'")
	easynews_results = [str(i[0]) for i in dbcur.fetchall()]
	if not easynews_results: return 'success'
	try:
		dbcur.execute("DELETE FROM maincache WHERE id LIKE 'fen_EASYNEWS_SEARCH_%'")
		dbcon.commit()
		for i in easynews_results: window.clearProperty(i)
		return 'success'
	except: return 'failed'

