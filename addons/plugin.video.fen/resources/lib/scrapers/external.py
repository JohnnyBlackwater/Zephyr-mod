# -*- coding: utf-8 -*-
import json
import time
from importlib import import_module
from threading import Thread
from windows import create_window
from caches.providers_cache import providerCache
from modules import source_utils
from modules.debrid import debrid_check
from modules.kodi_utils import hide_busy_dialog, notification, sleep, monitor, window, local_string as ls
from modules.utils import clean_file_name, base32_to_hex, to_utf8, get_datetime, jsondate_to_datetime, adjust_premiered_date
from modules.settings import display_sleep_time, date_offset
from modules.settings_reader import get_setting
# from modules.kodi_utils import logger

pack_check = ('season', 'show')
pack_display = '%s (%s)'
total_format = '[COLOR %s][B]%s[/B][/COLOR]'
diag_format = '4K: %s | 1080p: %s | 720p: %s | SD: %s | %s: %s'

class ExternalSource:
	def __init__(self, source_dict, debrid_torrents, debrid_hosters, internal_scrapers, prescrape_sources, display_uncached_torrents, progress_dialog, disabled_ignored=False):
		hide_busy_dialog()
		self.scrape_provider = 'external'
		self.source_dict = source_dict
		self.debrid_torrents = debrid_torrents
		self.debrid_hosters = debrid_hosters
		self.internal_scrapers = internal_scrapers
		self.prescrape_sources = prescrape_sources
		self.display_uncached_torrents = display_uncached_torrents
		self.progress_dialog = progress_dialog
		self.disabled_ignored = disabled_ignored
		self.internal_activated = len(self.internal_scrapers) > 0
		self.internal_prescraped = len(self.prescrape_sources) > 0
		self.processed_prescrape = False
		self.scraping_started = False
		self.sources = []
		self.final_sources = []
		self.processed_internal_scrapers = []
		self.meta = json.loads(window.getProperty('fen_playback_meta'))
		self.background = self.meta.get('background', False)
		self.hostDict = self.make_host_dict()
		self.source_dict_pack = source_utils.get_pack_sources()
		self.sleep_time = display_sleep_time()
		self.int_dialog_highlight = get_setting('int_dialog_highlight', 'darkgoldenrod')
		self.ext_dialog_highlight = get_setting('ext_dialog_highlight', 'dodgerblue')
		self.finish_early = get_setting('search.finish.early') == 'true'
		self.int_total_format = total_format % (self.int_dialog_highlight, '%s')
		self.ext_total_format = total_format % (self.ext_dialog_highlight, '%s')
		self.timeout = 60 if self.disabled_ignored else int(get_setting('scrapers.timeout.1', '60'))
		self.internal_sources_total = self.internal_sources_4K = self.internal_sources_1080p = self.internal_sources_720p = self.internal_sources_sd = 0
		self.sources_total = self.sources_4k = self.sources_1080p = self.sources_720p = self.sources_sd = 0

	def results(self, info):
		results = []
		self.db_type = info['db_type']
		self.orig_title = info['title']
		self.tmdb_id = str(info['tmdb_id'])
		self.season, self.episode = info['season'], info['episode']
		self.total_seasons = info['total_seasons']
		self.title = source_utils.normalize(info['title'])
		self.year = info['year']
		self.premiered = info['premiered']
		ep_name = source_utils.normalize(info['ep_name'])
		aliases = info['aliases']
		if self.db_type == 'movie':
			self.data = {'imdb': info['imdb_id'], 'title': self.title, 'aliases': aliases, 'year': str(self.year)}
		else:
			self.data = {'imdb': info['imdb_id'], 'tvdb': info['tvdb_id'], 'tvshowtitle': self.title, 'aliases': aliases,'year': str(self.year),
						'title': ep_name, 'premiered': info['premiered'], 'season': str(self.season), 'episode': str(self.episode)}
		results = self.get_sources()
		return results

	def get_sources(self):
		def _scraperDialog():
			while not self.scraping_started:
				if len([x for x in threads if x.is_alive()]) == 0: return
				sleep(5)
			self.make_progress_dialog()
			string1, string2 = ls(32676), ls(32677)
			if self.internal_activated or self.internal_prescraped:
				string3 = '[COLOR %s][B]Int:[/B][/COLOR]%s' % (self.int_dialog_highlight, '%s')
				string4 = '[COLOR %s][B]Ext:[/B][/COLOR]%s' % (self.ext_dialog_highlight, '%s')
			else:
				string4 = '[COLOR %s][B]%s[/B][/COLOR]' % (self.ext_dialog_highlight, ls(32118))
			line = '%s[CR]%s[CR]%s'
			line1 = line2 = line3 = ''
			start_time = time.time()
			end_time = start_time + self.timeout
			close_dialog = True
			while not self.progress_dialog.iscanceled():
				try:
					if monitor.abortRequested() is True: break
					self.process_internal_results()
					internalSource_4k_label = self.int_total_format % self.internal_sources_4K
					internalSource_1080_label = self.int_total_format % self.internal_sources_1080p
					internalSource_720_label = self.int_total_format % self.internal_sources_720p
					internalSource_sd_label = self.int_total_format % self.internal_sources_sd
					internalSource_total_label = self.int_total_format % self.internal_sources_total
					source_4k_label = self.ext_total_format % self.sources_4k
					source_1080_label = self.ext_total_format % self.sources_1080p
					source_720_label = self.ext_total_format % self.sources_720p
					source_sd_label = self.ext_total_format % self.sources_sd
					source_total_label = self.ext_total_format % self.sources_total
					current_time = time.time()
					current_progress = max((current_time - start_time), 0)
					try:
						info = [x.getName() for x in threads if x.is_alive()]
						percent = int((current_progress/float(self.timeout))*100)
						if self.internal_activated or self.internal_prescraped:
							info.extend([i for i in self.internal_scrapers if not i in self.processed_internal_scrapers])
							line1 = string3 % diag_format % (internalSource_4k_label, internalSource_1080_label,
													  		internalSource_720_label, internalSource_sd_label, string2, internalSource_total_label)
							line2 = string4 % diag_format % (source_4k_label, source_1080_label, source_720_label, source_sd_label, string2, source_total_label)
						else:
							line1 = string4
							line2 = diag_format % (source_4k_label, source_1080_label, source_720_label, source_sd_label, string2, source_total_label)
						len_alive_threads = len(info)
						if len_alive_threads > 6: line3 = string1 % str(len_alive_threads)
						else: line3 = string1 % ', '.join(info).upper()
						self.progress_dialog.update(line % (line1, line2, line3), percent)
						sleep(self.sleep_time)
						if self.finish_early:
							if percent >= 50:
								if len_alive_threads <= 5: close_dialog = False; break
								if len(self.sources) >= 100 * len_alive_threads: close_dialog = False; break
						if len_alive_threads == 0: close_dialog = False; break
						if end_time < current_time: close_dialog = False; break
					except: pass
				except Exception: pass
			if close_dialog: self.kill_progress_dialog()
			return
		def _background():
			start_time = time.time()
			end_time = start_time + self.timeout
			while time.time() < end_time:
				alive_threads = [x.getName() for x in threads if x.is_alive()]
				sleep(self.sleep_time)
				if len(alive_threads) <= 5: return
				if len(self.sources) >= 100 * len(alive_threads): return
		self.get_expiry_hours()
		source_dict = [i for i in self.source_dict]
		if self.db_type == 'movie':
			threads = list(self.process_movie_threads(source_dict))
		else:
			self.season_packs, self.show_packs = source_utils.pack_enable_check(self.meta, self.season, self.episode)
			if self.season_packs: source_dict.extend([(i[0], i[1], 'season') for i in self.source_dict if i[0] in self.source_dict_pack])
			if self.show_packs: source_dict.extend([(i[0], i[1], 'show') for i in self.source_dict if i[0] in self.source_dict_pack])
			threads = list(self.process_episode_threads(source_dict))
		if self.background: _background()
		else: _scraperDialog()
		self.final_sources.extend(self.sources)
		self.process_duplicates()
		self.process_filters()
		return self.final_sources

	def get_movie_source(self, provider, module_path):
		sources = providerCache.get(provider, self.db_type, self.tmdb_id, self.title, self.year, '', '')
		if sources == None:
			module = import_module(module_path)
			call = module.source()
			if not call.movie: return
			self.scraping_started = True
			sources = call.sources(self.data, self.hostDict)
			sources = self.process_sources(provider, sources)
			providerCache.set(provider, self.db_type, self.tmdb_id, self.title, self.year, '', '', sources, self.single_expiry)
		if sources:
			self.process_quality_count(sources)
			self.sources.extend(sources)

	def get_episode_source(self, provider, module_path, pack):
		if pack in pack_check:
			if pack == 'show': s_check = ''
			else: s_check = self.season
			e_check = ''
		else: s_check, e_check = self.season, self.episode
		sources = providerCache.get(provider, self.db_type, self.tmdb_id, self.title, self.year, s_check, e_check)
		if sources == None:
			module = import_module(module_path)
			call = module.source()
			if not call.tvshow: return
			self.scraping_started = True
			if pack == 'show':
				expiry_hours = self.show_expiry
				sources = call.sources_packs(self.data, self.hostDict, search_series=True, total_seasons=self.total_seasons)
			elif pack == 'season':
				expiry_hours = self.season_expiry
				sources = call.sources_packs(self.data, self.hostDict)
			else:
				expiry_hours = self.single_expiry
				sources = call.sources(self.data, self.hostDict)
			sources = self.process_sources(provider, sources)
			providerCache.set(provider, self.db_type, self.tmdb_id, self.title, self.year, s_check, e_check, sources, expiry_hours)
		if sources:
			if pack == 'show': sources = [i for i in sources if i.get('last_season') >= self.season]
			self.process_quality_count(sources)
			self.sources.extend(sources)

	def get_expiry_hours(self):
		try:
			current_date = get_datetime()
			if self.db_type == 'movie':
				premiered = jsondate_to_datetime(self.premiered, '%Y-%m-%d', remove_time=True)
				difference = (current_date - premiered).days
				if difference == 0: self.single_expiry = int(24*0.125)
				elif difference <= 10: self.single_expiry = 24*1
				elif difference <= 14: self.single_expiry = 24*3
				elif difference <= 180: self.single_expiry = 24*180
				else: self.single_expiry = 24*365
			else:
				ended = self.meta['extra_info']['status'].lower() in ('ended', 'canceled')
				premiered = adjust_premiered_date(self.premiered, date_offset())[0]
				difference = (current_date - premiered).days
				last_episode_to_air = jsondate_to_datetime(self.meta['extra_info']['last_episode_to_air']['air_date'], '%Y-%m-%d', remove_time=True)
				last_ep_difference = (current_date - last_episode_to_air).days
				if ended:
					if last_ep_difference <= 30: recently_ended = True
					else: recently_ended = False
				if not ended or recently_ended:
					if difference == 0: self.single_expiry = int(24*0.125)
					elif difference <= 3: self.single_expiry = 24*1
					elif difference <= 7: self.single_expiry = 24*3
					elif difference <= 14: self.single_expiry = 24*14
					elif difference <= 28: self.single_expiry = 24*180
					else: self.single_expiry = 24*365
					if self.meta['total_seasons'] == self.season and last_ep_difference <= 21: self.season_expiry = 24*10
					else: self.season_expiry = 24*365
					self.show_expiry = 24*10
				else:
					self.single_expiry = 24*365
					self.season_expiry = 24*365
					self.show_expiry = 24*365
		except: self.single_expiry, self.season_expiry,  self.show_expiry = 24, 336, 336

	def process_movie_threads(self, source_dict):
		for i in source_dict:
			provider, module_path = i[0], i[1]
			threaded_object = Thread(target=self.get_movie_source, args=(provider, module_path), name=provider)
			threaded_object.start()
			yield threaded_object

	def process_episode_threads(self, source_dict):
		for i in source_dict:
			provider, module_path, pack_arg = i[0], i[1], i[2]
			if pack_arg: provider_display = pack_display % (i[0], i[2])
			else: provider_display = provider
			threaded_object = Thread(target=self.get_episode_source, args=(provider, module_path, pack_arg), name=provider_display)
			threaded_object.start()
			yield threaded_object

	def process_duplicates(self):
		def _process(sources):
			uniqueURLs = set()
			uniqueHashes = set()
			for provider in sources:
				try:
					url = provider['url'].lower()
					if url not in uniqueURLs:
						uniqueURLs.add(url)
					if 'hash' in provider:
						if provider['hash'] not in uniqueHashes:
							uniqueHashes.add(provider['hash'])
							yield provider
					else: yield provider
				except: yield provider
		if len(self.final_sources) > 0: self.final_sources = list(_process(self.final_sources))

	def process_filters(self):
		def _process(result_list, target):
			for item in result_list:
				obj = Thread(target=target, args=(item,))
				obj.start()
				append(obj)
		def _process_torrents(item):
			if item in ('Real-Debrid', 'Premiumize.me', 'AllDebrid'):
				self.filter += [dict(i, **{'debrid':item}) for i in torrentSources if item == i.get('cache_provider')]
				if self.display_uncached_torrents:
					self.filter += [dict(i, **{'debrid':item}) for i in torrentSources if 'Uncached' in i.get('cache_provider') and item in i.get('cache_provider')]
		def _process_hosters(item):
			for k, v in item.items():
				valid_hosters = [i for i in result_hosters if i in v]
				self.filter += [dict(i, **{'debrid':k}) for i in hoster_sources if i['source'] in valid_hosters]
		threads = []
		append = threads.append
		self.filter = []
		hoster_sources = [i for i in self.final_sources if not 'hash' in i]
		torrentSources = self.process_torrents([i for i in self.final_sources if not i in hoster_sources])
		result_hosters = list(set([i['source'].lower() for i in hoster_sources]))
		if self.debrid_torrents: _process(self.debrid_torrents, _process_torrents)
		if self.debrid_hosters: _process(self.debrid_hosters, _process_hosters)
		[i.join() for i in threads]
		self.final_sources = self.filter

	def process_sources(self, provider, sources):
		try:
			for i in sources:
				try:
					if 'hash' in i:
						_hash = i['hash'].lower()
						i['hash'] = str(_hash)
					size, size_label, divider = 0, None, None
					if 'name' in i: URLName = clean_file_name(i['name']).replace('html', ' ').replace('+', ' ').replace('-', ' ')
					else: URLName = source_utils.get_filename_match(self.orig_title, i['url'], i.get('name', None))
					if 'name_info' in i: quality, extraInfo = source_utils.get_file_info(name_info=i['name_info'])
					else: quality, extraInfo = source_utils.get_file_info(url=i['url'])
					try:
						size = i['size']
						if 'package' in i:
							if i['package'] == 'season': divider = [int(x['episode_count']) for x in self.meta['season_data'] if int(x['season_number']) == int(self.meta['season'])][0]
							else: divider = int(self.meta['total_aired_eps'])
							size = float(size) / divider
							size_label = '%.2f GB' % size
						else:
							size_label = '%.2f GB' % size
					except: pass
					i.update({'provider': provider, 'external': True, 'scrape_provider': self.scrape_provider, 'extraInfo': extraInfo,
								'URLName': URLName, 'quality': quality, 'size_label': size_label, 'size': round(size, 2)})
				except: pass
		except: pass
		return sources
	
	def process_quality_count(self, sources, internal=False):
		if internal:
			for i in sources:
				quality = i['quality']
				if quality == '4K': self.internal_sources_4K += 1
				elif quality in ['1440p', '1080p']: self.internal_sources_1080p += 1
				elif quality in ['720p', 'HD']: self.internal_sources_720p += 1
				else: self.internal_sources_sd += 1
				self.internal_sources_total += 1
		else:
			for i in sources:
				quality = i['quality']
				if quality == '4K': self.sources_4k += 1
				elif quality == '1080p': self.sources_1080p += 1
				elif quality == '720p': self.sources_720p += 1
				else: self.sources_sd += 1
				self.sources_total += 1

	def process_torrents(self, torrentSources):
		def _return_early(return_list=torrentSources):
			try: self.kill_progress_dialog()
			except: pass
			return return_list
		if len(torrentSources) == 0: return _return_early()
		if len(self.debrid_torrents) == 0: return _return_early([])
		hashList = []
		append = hashList.append
		for i in torrentSources:
			try:
				infoHash = i['hash']
				if len(infoHash) == 40:
					append(infoHash)
				else:
					converted_hash = base32_to_hex(infoHash)
					if converted_hash: append(converted_hash)
					else: torrentSources.remove(i)
			except: torrentSources.remove(i)
		if len(torrentSources) == 0: return _return_early()
		try:
			torrent_results = []
			hashList = list(set(hashList))
			cached_hashes = debrid_check.run(hashList, self.background, self.debrid_torrents, self.meta, self.progress_dialog)
			for item in [('Real-Debrid', 'rd_cached_hashes'), ('Premiumize.me', 'pm_cached_hashes'), ('AllDebrid', 'ad_cached_hashes')]:
				if item[0] in self.debrid_torrents:
					torrent_results.extend([dict(i, **{'cache_provider':item[0]}) for i in torrentSources if i['hash'] in cached_hashes[item[1]]])
					if self.display_uncached_torrents:
						torrent_results.extend([dict(i, **{'cache_provider':'Uncached %s' % item[0]}) for i in torrentSources if not i['hash'] in cached_hashes[item[1]]])
			return torrent_results
		except:
			self.kill_progress_dialog()
			notification(32574, 2500)

	def process_internal_results(self):
		if self.internal_prescraped and not self.processed_prescrape:
			self.process_quality_count(self.prescrape_sources, internal=True)
			self.processed_prescrape = True
		append = self.processed_internal_scrapers.append
		for i in self.internal_scrapers:
			win_property = window.getProperty('%s.internal_results' % i)
			if win_property in ('checked', '', None): continue
			try: internal_sources = json.loads(win_property)
			except: continue
			window.setProperty('%s.internal_results' % i, 'checked')
			append(i)
			self.process_quality_count(internal_sources, internal=True)

	def make_host_dict(self):
		pr_list = []
		for item in self.debrid_hosters:
			for k, v in item.items():
				pr_list += v
		return list(set(pr_list))

	def make_progress_dialog(self):
		if not self.progress_dialog:
			self.progress_dialog = create_window(('windows.yes_no_progress_media', 'YesNoProgressMedia'), 'yes_no_progress_media.xml', meta=self.meta)
			Thread(target=self.progress_dialog.run).start()
		if self.disabled_ignored: self.progress_dialog.update('[CR][B]%s....[/B]' % ls(32678))

	def kill_progress_dialog(self):
		try: self.progress_dialog.close()
		except: pass
		try: del self.progress_dialog
		except: pass
		self.progress_dialog = None
