# -*- coding: utf-8 -*-
import time
import json
from threading import Thread
from sys import exit as sysexit
try: from urllib import unquote
except ImportError: from urllib.parse import unquote
import metadata
from windows import open_window, create_window
from scrapers.external import ExternalSource
from scrapers.folder_scraper import FolderScraper
from modules import debrid
from modules import resolver
from modules import kodi_utils
from modules import settings
from modules.player import FenPlayer
from modules.source_utils import sources, scraper_names
from modules.utils import clean_file_name, string_to_float, to_utf8, safe_string, remove_accents
from modules.settings_reader import get_setting
# from modules.kodi_utils import logger

ls = kodi_utils.local_string
window = kodi_utils.window
cloud_scrapers = ('rd-cloud', 'pm-cloud', 'ad-cloud')
folder_scrapers = ('folder1', 'folder2', 'folder3', 'folder4', 'folder5')
default_internal_scrapers = ('furk', 'easynews', 'rd-cloud', 'pm-cloud', 'ad-cloud', 'folder1', 'folder2', 'folder3', 'folder4', 'folder5')
hevc_filter_key, hdr_filter_key, dolby_vision_filter_key = '[B]HEVC[/B]', '[B]HDR[/B]', '[B]D/VISION[/B]'
diag_format = '[COLOR %s][B]%s[/B][/COLOR] 4K: %s | 1080p: %s | 720p: %s | SD: %s | Total: %s'

class Sources():
	def __init__(self):
		self.filters_ignored = False
		self.progress_dialog = None
		self.params = {}
		self.threads = []
		self.providers = []
		self.sources = []
		self.prescrape_scrapers = []
		self.prescrape_threads = []
		self.prescrape_sources = []
		self.remove_scrapers = []
		self.prescrape = 'true'
		self.disabled_ignored = 'false'
		self.exclude_list = ['furk', 'easynews', 'ororo', 'filepursuit', 'library', 'gdrive']# leave as list you idiot.
		self.sourcesTotal = self.sources4K = self.sources1080p = self.sources720p = self.sourcesSD = 0
		self.language = get_setting('meta_language')

	def playback_prep(self, params=None):
		self._clear_properties()
		if params: self.params = params
		self.vid_type = self.params['vid_type']
		self.tmdb_id = self.params['tmdb_id']
		self.ep_name = self.params.get('ep_name')
		self.plot = self.params.get('plot')
		self.prescrape = self.params.get('prescrape', self.prescrape) == 'true'
		self.background = self.params.get('background', 'false') == 'true'
		self.disabled_ignored = self.params.get('disabled_ignored', self.disabled_ignored) == 'true'
		self.from_library = self.params.get('library', 'False') == 'True'
		self.custom_title = self.params.get('custom_title', None)
		self.custom_year = self.params.get('custom_year', None)
		if 'remove_scrapers' in self.params: self.remove_scrapers = json.loads(self.params['remove_scrapers'])
		if 'prescrape_sources' in self.params: self.prescrape_sources = json.loads(self.params['prescrape_sources'])
		if 'autoplay' in self.params: self.autoplay = self.params.get('autoplay', 'False') == 'True'
		else: self.autoplay = settings.auto_play(self.vid_type)
		if 'season' in self.params: self.season = int(self.params['season'])
		else: self.season = ''
		if 'episode' in self.params: self.episode = int(self.params['episode'])
		else: self.episode = ''
		if 'meta' in self.params: self.meta = json.loads(self.params['meta'])
		else: self._grab_meta()
		self.active_scrapers = settings.active_scrapers()
		self.provider_sort_ranks = settings.provider_sort_ranks()
		self.sleep_time = settings.display_sleep_time()
		self.scraper_settings = settings.scraping_settings()
		self.include_prerelease_results = settings.include_prerelease_results()
		self.ignore_filters = settings.ignore_results_filter()
		self.filter_hevc = settings.filter_status('hevc')
		self.filter_hdr = settings.filter_status('hdr')
		self.filter_dv = settings.filter_status('dv')
		self.sort_keys = settings.results_sort_order()
		self.display_uncached_torrents = settings.display_uncached_torrents()
		self.quality_filter = self._quality_filter()
		self.filter_size = get_setting('results.filter.size', '0') == 'true'
		self.include_unknown_size = get_setting('results.include.unknown.size') == 'true'
		self.include_3D_results = get_setting('include_3d_results') == 'true'
		self._update_meta()
		self._search_info()
		window.setProperty('fen_playback_meta', json.dumps(self.meta))
		kodi_utils.hide_busy_dialog()
		self.get_sources()

	def get_sources(self):
		results = []
		self.active_scrapers = [i for i in self.active_scrapers if not i in self.remove_scrapers]
		if any(x in self.active_scrapers for x in default_internal_scrapers):
			if self.prescrape:
				results = self.pre_scrape_check()
				if results: results = self.process_results(results)
		if not results:
			self.prescrape = False
			if 'external' in self.active_scrapers:
				self.activate_debrid_info()
				self.activate_external_providers()
			self.orig_results = self.collect_results()
			results = self.process_results(self.orig_results)
			if not results: return self._process_post_results()
		kodi_utils.hide_busy_dialog()
		self.play_source(results)

	def collect_results(self):
		append = self.providers.append
		if any(x in folder_scrapers for x in self.active_scrapers):
			self.check_folder_scrapers(self.active_scrapers, self.providers, False)
		if 'furk' in self.active_scrapers:
			from scrapers.furk import FurkSource
			append(('furk', FurkSource()))
		if 'easynews' in self.active_scrapers:
			from scrapers.easynews import EasyNewsSource
			append(('easynews', EasyNewsSource()))
		if 'pm-cloud' in self.active_scrapers:
			from scrapers.pm_cache import PremiumizeSource
			append(('pm-cloud', PremiumizeSource()))
		if 'rd-cloud' in self.active_scrapers:
			from scrapers.rd_cache import RealDebridSource
			append(('rd-cloud', RealDebridSource()))
		if 'ad-cloud' in self.active_scrapers:
			from scrapers.ad_cache import AllDebridSource
			append(('ad-cloud', AllDebridSource()))
		if 'external' in self.active_scrapers:
			internal_scrapers = self.active_scrapers[:]
			internal_scrapers.remove('external')
			if not internal_scrapers: internal_scrapers = []
		append = self.threads.append
		if self.providers:
			for i in range(len(self.providers)):
				append(Thread(target=self.activate_providers, args=(self.providers[i][1], False), name=self.providers[i][0]))
			[i.start() for i in self.threads]
		self.sources.extend(self.prescrape_sources)
		if 'external' in self.active_scrapers or self.background:
			if 'external' in self.active_scrapers:
				internal_scrapers = self.get_folderscraper_names(internal_scrapers)
				self.activate_providers(ExternalSource(self.external_providers, self.debrid_torrent_enabled, self.debrid_valid_hosts, internal_scrapers,
														self.prescrape_sources, self.display_uncached_torrents, self.progress_dialog, self.disabled_ignored), False)
			if self.providers:
				[i.join() for i in self.threads]
		else:
			self.scrapers_dialog('internal')
		return self.sources

	def process_results(self, results):
		if self.prescrape: self.all_scrapers = self.active_scrapers
		else: self.all_scrapers = self.active_scrapers + self.remove_scrapers
		results = self.filter_results(results)
		results = self.sort_results(results)
		results = self._special_sort(results, hevc_filter_key, self.filter_hevc)
		results = self._special_sort(results, hdr_filter_key, self.filter_hdr)
		results = self._special_sort(results, dolby_vision_filter_key, self.filter_dv)
		results = self._sort_first(results)
		return results

	def filter_results(self, results):
		results = [i for i in results if i['quality'] in self.quality_filter]
		if not self.include_3D_results: results = [i for i in results if not '3D' in i['extraInfo']]
		if self.filter_size:
			duration = self.meta['duration'] or (5400 if self.vid_type == 'movie' else 2400)
			max_size = ((0.125 * (0.90 * string_to_float(get_setting('results.size.auto', '20'), '20'))) * duration)/1000
			if self.include_unknown_size: results = [i for i in results if i['scrape_provider'].startswith('folder') or i['size'] <= max_size]
			else: results = [i for i in results if i['scrape_provider'].startswith('folder') or 0.01 < i['size'] <= max_size]
		return results

	def sort_results(self, results):
		def _add_keys(item):
			provider = item['scrape_provider']
			if 'folder' in provider: provider = 'files'
			if provider == 'external':
				try: account_type = item['debrid'].lower()
				except: account_type = 'free'
			else: account_type = provider.lower()
			item['provider_rank'] = self._get_provider_rank(account_type)
			item['quality_rank'] = self._get_quality_rank(item.get('quality', 'SD'))
		for item in results: _add_keys(item)
		for item in reversed(self.sort_keys):
			if item == 'size': reverse = True
			else: reverse = False
			results.sort(key=lambda k: k[item], reverse=reverse)
		if self.display_uncached_torrents: results = self._sort_uncached_torrents(results)
		return results

	def activate_providers(self, function, prescrape):
		sources = function.results(self.search_info)
		if sources:
			self._sources_quality_count(sources)
			if prescrape: self.prescrape_sources.extend(sources)
			else: self.sources.extend(sources)

	def activate_external_providers(self):
		external_providers = sources(self.disabled_ignored)
		if self.debrid_torrent_enabled == []:
			torrent_scrapers = scraper_names('torrents')
			self.exclude_list.extend(torrent_scrapers)
		if self.debrid_valid_hosts == []:
			hoster_scrapers = scraper_names('hosters')
			self.exclude_list.extend(hoster_scrapers)
		self.external_providers = [i for i in external_providers if not i[0] in self.exclude_list]

	def activate_debrid_info(self):
		self.debrid_enabled = debrid.debrid_enabled()
		debrid_hoster_enabled = debrid.debrid_type_enabled('hoster', self.debrid_enabled)
		self.debrid_torrent_enabled = debrid.debrid_type_enabled('torrent', self.debrid_enabled)
		self.debrid_valid_hosts = debrid.debrid_valid_hosts(debrid_hoster_enabled)

	def play_source(self, results):
		if self.background: return self.play_execute_nextep(results)
		if self.autoplay: return self.play_file(results, autoplay=True)
		return self.display_results(results)

	def pre_scrape_check(self):
		prescrape_append = self.prescrape_scrapers.append
		remove_append = self.remove_scrapers.append
		threads_append = self.prescrape_threads.append
		if self.autoplay:
			if any(x in folder_scrapers for x in self.active_scrapers):
				self.check_folder_scrapers(self.active_scrapers, self.prescrape_scrapers, False)
				self.remove_scrapers.extend(folder_scrapers)
		else:
			if any(x in folder_scrapers for x in self.active_scrapers) and settings.check_prescrape_sources('folders'):
				self.check_folder_scrapers(self.active_scrapers, self.prescrape_scrapers)
				self.remove_scrapers.extend(folder_scrapers)
		if 'furk' in self.active_scrapers and settings.check_prescrape_sources('furk'):
			from scrapers.furk import FurkSource
			prescrape_append(('furk', FurkSource()))
			remove_append('furk')
		if 'easynews' in self.active_scrapers and settings.check_prescrape_sources('easynews'):
			from scrapers.easynews import EasyNewsSource
			prescrape_append(('easynews', EasyNewsSource()))
			remove_append('easynews')
		if 'rd-cloud' in self.active_scrapers and settings.check_prescrape_sources('rd-cloud'):
			from scrapers.rd_cache import RealDebridSource
			prescrape_append(('rd-cloud', RealDebridSource()))
			remove_append('rd-cloud')
		if 'pm-cloud' in self.active_scrapers and settings.check_prescrape_sources('pm-cloud'):
			from scrapers.pm_cache import PremiumizeSource
			prescrape_append(('pm-cloud', PremiumizeSource()))
			remove_append('pm-cloud')
		if 'ad-cloud' in self.active_scrapers and settings.check_prescrape_sources('ad-cloud'):
			from scrapers.ad_cache import AllDebridSource
			prescrape_append(('ad-cloud', AllDebridSource()))
			remove_append('ad-cloud')
		len_prescrape_scrapers = len(self.prescrape_scrapers)
		if len_prescrape_scrapers == 0: return []
		for i in range(len_prescrape_scrapers):
			threads_append(Thread(target=self.activate_providers, args=(self.prescrape_scrapers[i][1], True), name=self.prescrape_scrapers[i][0]))
		[i.start() for i in self.prescrape_threads]
		if self.background:
			[i.join() for i in self.prescrape_threads]
		else:
			self.scrapers_dialog('pre_scrape')
		return self.prescrape_sources

	def check_folder_scrapers(self, active_scrapers, append_list, prescrape=True):
		append = append_list.append
		for i in active_scrapers:
			if i.startswith('folder'):
				scraper_name = get_setting('%s.display_name' % i)
				if prescrape:
					if settings.check_prescrape_sources('folders'): append((scraper_name, FolderScraper(i, scraper_name)))
				else: append((scraper_name, FolderScraper(i, scraper_name)))

	def get_folderscraper_names(self, internal_scrapers):
		append = internal_scrapers.append
		folder_scrapers = [i for i in internal_scrapers if i.startswith('folder')]
		if not folder_scrapers: return internal_scrapers
		internal_scrapers = [i for i in internal_scrapers if not i in folder_scrapers]
		for i in folder_scrapers: append(get_setting('%s.display_name' % i))
		return internal_scrapers

	def scrapers_dialog(self, scrape_type):
		def _scraperDialog():
			close_dialog = True
			while not self.progress_dialog.iscanceled():
				try:
					if kodi_utils.monitor.abortRequested() is True: return sysexit()
					remaining_providers = [x.getName() for x in _threads if x.is_alive() is True]
					s4k_label = total_format % self.sources4K
					s1080_label = total_format % self.sources1080p
					s720_label = total_format % self.sources720p
					ssd_label = total_format % self.sourcesSD
					stotal_label = total_format % self.sourcesTotal
					try:
						current_time = time.time()
						current_progress = current_time - start_time
						line2 = diag_format % (int_dialog_hl, line2_inst, s4k_label, s1080_label, s720_label, ssd_label, stotal_label)
						if len(remaining_providers) > 3: line3_insert = str(len(remaining_providers))
						else: line3_insert = ', '.join(remaining_providers).upper()
						line3 = remaining_providers_str % line3_insert
						percent = int((current_progress/float(timeout))*100)
						self.progress_dialog.update(line % (line1, line2, line3), percent)
						kodi_utils.sleep(self.sleep_time)
						if len(remaining_providers) == 0: close_dialog = False; break
						if end_time < current_time: close_dialog = False; break
					except: pass
				except: pass
			if close_dialog or scrape_type == 'internal': self._kill_progress_dialog()
		kodi_utils.hide_busy_dialog()
		timeout = 25
		remaining_providers_str = ls(32676)
		line = '%s[CR]%s[CR]%s'
		int_dialog_hl = get_setting('int_dialog_highlight')
		if not int_dialog_hl or int_dialog_hl == '': int_dialog_hl = 'dodgerblue'
		total_format = '[COLOR %s][B]%s[/B][/COLOR]' % (int_dialog_hl, '%s')
		if scrape_type == 'internal':
			_threads = self.threads
			line1_inst = ls(32096)
			line2_inst = 'Int:'
		else:
			_threads = self.prescrape_threads
			line1_inst = '%s %s' % (ls(32829), ls(32830))
			line2_inst = 'Pre:'
		line1 = '[COLOR %s][B]%s[/B][/COLOR]' % (int_dialog_hl, line1_inst)
		start_time = time.time()
		end_time = start_time + timeout
		self._make_progress_dialog()
		_scraperDialog()

	def display_results(self, results):
		window_style = settings.results_xml_style()
		action, chosen_item = open_window(('windows.sources', 'SourceResults'), 'sources_results.xml',
							window_style=window_style, window_id=settings.results_xml_window_number(window_style), results=results,
							meta=self.meta, scraper_settings=self.scraper_settings, prescrape=self.prescrape, filters_ignored=self.filters_ignored)
		if not action and self.prescrape: self._kill_progress_dialog()
		if action == 'play':
			if self.prescrape: self._kill_progress_dialog()
			return self.play_file(results, chosen_item)
		elif self.prescrape and action == 'perform_full_search':
			self.params['prescrape'] = 'false'
			self.params['prescrape_sources'] = json.dumps(self.prescrape_sources)
			self.params['remove_scrapers'] = json.dumps(self.remove_scrapers)
			return self.playback_prep()

	def play_execute_nextep(self, results):
		nextep_url = self.play_file(results, autoplay=True, background=True)
		window.setProperty('fen_nextep_url', nextep_url)

	def _process_post_results(self):
		if self.ignore_filters and self.orig_results: return self._process_ignore_filters()
		return self._no_results()

	def _process_ignore_filters(self):
		self.filters_ignored = True
		orig_results = [i for i in self.orig_results if not i in self.prescrape_sources]
		orig_results.extend(self.prescrape_sources)
		if self.autoplay:
			orig_results = [i for i in orig_results if not 'Uncached' in i.get('cache_provider', '')]
			if self.filter_size:
				duration = self.meta['duration'] or (5400 if self.vid_type == 'movie' else 2400)
				min_size = 0
				max_size = ((0.125 * (0.90 * string_to_float(get_setting('results.size.auto', '20'), '20'))) * duration)/1000
				orig_results.sort(key=lambda x: x['size'])
				size_list = [i['size'] for i in orig_results]
				nearest_min_index = size_list.index(min(size_list, key=lambda x: abs(x - min_size)))
				nearest_max_index = size_list.index(min(size_list, key=lambda x: abs(x - max_size)))
				nearest_min_results = sorted(orig_results[:nearest_min_index + 1], key=lambda x: x['size'], reverse=True)[:5]
				nearest_max_results = sorted(orig_results[nearest_max_index:], key=lambda x: x['size'])[:5]
				orig_results = nearest_min_results + nearest_max_results
			include_quality = [i for i in orig_results if i['quality'] in self.quality_filter]
			exclude_quality = [i for i in orig_results if not i['quality'] in self.quality_filter]
			results = include_quality + exclude_quality
		else:
			results = self.sort_results(orig_results)
		if self.autoplay: kodi_utils.notification(32686)
		return self.play_source(results)

	def _no_results(self):
		kodi_utils.hide_busy_dialog()
		if self.background: return kodi_utils.notification('%s %s' % (ls(32801), ls(32760)), 5000)
		kodi_utils.notification(32760)

	def _update_meta(self):
		if self.from_library: self.meta.update({'plot': self.plot if self.plot else self.meta.get('plot'), 'from_library': self.from_library, 'ep_name': self.ep_name})
		self.meta.update({'vid_type': self.vid_type, 'season': self.season, 'episode': self.episode, 'background': self.background})
		if self.custom_title: self.meta['custom_title'] = self.custom_title
		if self.custom_year: self.meta['custom_year'] = self.custom_year

	def _search_info(self):
		title = self._get_search_title(self.meta)
		year = self._get_search_year(self.meta)
		aliases = self._make_alias_dict(title)
		ep_name = self._get_ep_name()
		self.search_info = {'db_type': self.vid_type, 'title': title, 'year': year, 'tmdb_id': self.tmdb_id, 'imdb_id': self.meta.get('imdb_id'),
				'season': self.season, 'episode': self.episode, 'premiered': self.meta.get('premiered'), 'tvdb_id': self.meta.get('tvdb_id'),
				'aliases': aliases, 'ep_name': ep_name, 'total_seasons': self.meta.get('total_seasons', 1)}

	def _get_search_title(self, meta):
		if 'custom_title' in meta: search_title = meta['custom_title']
		else:
			if self.language == 'en': search_title = meta['title']
			else: search_title = meta['original_title']
			if '(' in search_title: search_title = search_title.split('(')[0]
		return search_title

	def _get_search_year(self, meta):
		if 'custom_year' in meta: year = meta['custom_year']
		else:
			year = meta.get('year')
			if self.vid_type == 'movie' and 'external' in self.active_scrapers:
				if get_setting('search.enable.yearcheck', 'false') == 'true':
					kodi_utils.show_busy_dialog()
					from apis.imdb_api import imdb_movie_year
					try: year = imdb_movie_year(meta.get('imdb_id'))
					except: pass
					kodi_utils.hide_busy_dialog()
		return year

	def _make_alias_dict(self, title):
		original_title = self.meta['original_title']
		alternative_titles = self.meta.get('alternative_titles', [])
		country_codes = set([i.replace('GB', 'UK') for i in self.meta.get('country_codes', [])])
		aliases = [{'title': i, 'country': ''} for i in alternative_titles]
		if original_title not in aliases: aliases.append({'title': original_title, 'country': ''})
		if country_codes: aliases.extend([{'title': '%s %s' % (title, i), 'country': ''} for i in country_codes])
		return aliases

	def _get_ep_name(self):
		ep_name = None
		if self.vid_type == 'episode':
			ep_name = self.meta.get('ep_name')
			try: ep_name = to_utf8(safe_string(remove_accents(ep_name)))
			except: ep_name = to_utf8(safe_string(ep_name))
		return ep_name
	
	def _sources_quality_count(self, sources):
		for i in sources:
			quality = i['quality']
			if quality == '4K': self.sources4K += 1
			elif quality in ['1440p', '1080p']: self.sources1080p += 1
			elif quality in ['720p', 'HD']: self.sources720p += 1
			else: self.sourcesSD += 1
			self.sourcesTotal += 1

	def _quality_filter(self):
		setting = 'results_quality_%s' % self.vid_type if not self.autoplay else 'autoplay_quality_%s' % self.vid_type
		quality_filter = settings.quality_filter(setting)
		if self.include_prerelease_results and 'SD' in quality_filter: quality_filter += ['SCR', 'CAM', 'TELE']
		return quality_filter

	def _get_quality_rank(self, quality):
		return {'4K': 1, '1080p': 2, '720p': 3, 'SD': 4, 'SCR': 5, 'CAM': 5, 'TELE': 5}[quality]

	def _get_provider_rank(self, account_type):
		return self.provider_sort_ranks[account_type] or 11

	def _sort_first(self, results):
		try:
			sort_first_scrapers = []
			if settings.sort_to_top('folders'): sort_first_scrapers.extend([i for i in self.all_scrapers if i in folder_scrapers])
			sort_first_scrapers.extend([i for i in self.all_scrapers if i in cloud_scrapers and settings.sort_to_top(i)])
			if not sort_first_scrapers: return results
			sort_first = [i for i in results if i['scrape_provider'] in sort_first_scrapers]
			sort_first.sort(key=lambda k: (self._sort_folder_to_top(k['scrape_provider']), k['quality_rank']))
			sort_last = [i for i in results if not i in sort_first]
			results = sort_first + sort_last
		except: pass
		return results

	def _sort_folder_to_top(self, provider):
		if provider in folder_scrapers: return 0
		else: return 1

	def _sort_uncached_torrents(self, results):
		uncached = [i for i in results if 'Uncached' in i.get('cache_provider', '')]
		results = [i for i in results if not i in uncached]
		return results + uncached

	def _special_sort(self, results, key, enable_setting):
		if enable_setting == 1:
			results = [i for i in results if not key in i['extraInfo']]
		elif enable_setting == 2 and self.autoplay:
			priority_list = [i for i in results if key in i['extraInfo']]
			remainder_list = [i for i in results if not i in priority_list]
			results = priority_list + remainder_list
		return results

	def _grab_meta(self):
		meta_user_info = metadata.retrieve_user_info(window)
		if self.vid_type == 'movie':
			self.meta = metadata.movie_meta('tmdb_id', self.tmdb_id, meta_user_info)
		else:
			self.meta = metadata.tvshow_meta('tmdb_id', self.tmdb_id, meta_user_info)
			episodes_data = metadata.season_episodes_meta(self.season, self.meta, meta_user_info)
			try:
				episode_data = [i for i in episodes_data if i['episode'] == int(self.episode)][0]
				self.meta.update({'vid_type': 'episode', 'season': episode_data['season'], 'episode': episode_data['episode'], 'premiered': episode_data['premiered'],
								'ep_name': episode_data['title'], 'plot': episode_data['plot']})
			except: pass

	def _clear_properties(self):
		for item in default_internal_scrapers: window.clearProperty('%s.internal_results' % item)

	def _make_progress_dialog(self):
		if not self.progress_dialog:
			self.progress_dialog = create_window(('windows.yes_no_progress_media', 'YesNoProgressMedia'), 'yes_no_progress_media.xml', meta=self.meta)
			Thread(target=self.progress_dialog.run).start()

	def _kill_progress_dialog(self):
		try: self.progress_dialog.close()
		except: kodi_utils.close_all_dialog()
		try: del self.progress_dialog
		except: pass
		self.progress_dialog = None

	def furkPacks(self, name, file_id, highlight=None, download=False):
		from apis.furk_api import FurkAPI
		kodi_utils.show_busy_dialog()
		t_files = FurkAPI().t_files(file_id)
		t_files = [i for i in t_files if 'video' in i['ct'] and 'bitrate' in i]
		t_files.sort(key=lambda k: k['name'].lower())
		kodi_utils.hide_busy_dialog()
		if download: return t_files
		default_furk_icon = kodi_utils.translate_path('special://home/addons/script.tikiart/resources/media/furk.png')
		list_items = [{'line1': '%.2f GB | %s' % (float(item['size'])/1073741824, clean_file_name(item['name']).upper()), 'icon': default_furk_icon} for item in t_files]
		kwargs = {'items': json.dumps(list_items), 'heading': name, 'highlight': highlight, 'enumerate': 'true', 'multi_choice': 'false', 'multi_line': 'false'}
		chosen_result = kodi_utils.select_dialog(t_files, **kwargs)
		if chosen_result is None: return None
		link = chosen_result['url_dl']
		name = chosen_result['name']
		return FenPlayer().run(link, 'video')

	def debridPacks(self, debrid_provider, name, magnet_url, info_hash, highlight=None, download=False):
		if debrid_provider == 'Real-Debrid':
			from apis.real_debrid_api import RealDebridAPI as debrid_function
			icon = 'realdebrid.png'
		elif debrid_provider == 'Premiumize.me':
			from apis.premiumize_api import PremiumizeAPI as debrid_function
			icon = 'premiumize.png'
		elif debrid_provider == 'AllDebrid':
			from apis.alldebrid_api import AllDebridAPI as debrid_function
			icon = 'alldebrid.png'
		kodi_utils.show_busy_dialog()
		try: debrid_files = debrid_function().display_magnet_pack(magnet_url, info_hash)
		except: debrid_files = None
		debrid_files.sort(key=lambda k: k['filename'].lower())
		kodi_utils.hide_busy_dialog()
		if not debrid_files: return kodi_utils.notification(32574)
		if download: return debrid_files, debrid_function
		default_debrid_icon = kodi_utils.translate_path('special://home/addons/script.tikiart/resources/media/%s' % icon)
		list_items = [{'line1': '%.2f GB | %s' % (float(item['size'])/1073741824, clean_file_name(item['filename']).upper()), 'icon': default_debrid_icon} for item in debrid_files]
		kwargs = {'items': json.dumps(list_items), 'heading': name, 'highlight': highlight, 'enumerate': 'true', 'multi_choice': 'false', 'multi_line': 'false'}
		chosen_result = kodi_utils.select_dialog(debrid_files, **kwargs)
		if chosen_result is None: return None
		url_dl = chosen_result['link']
		if debrid_provider in ('Real-Debrid', 'AllDebrid'):
			link = debrid_function().unrestrict_link(url_dl)
		elif debrid_provider == 'Premiumize.me':
			link = debrid_function().add_headers_to_url(url_dl)
		name = chosen_result['filename']
		return FenPlayer().run(link, 'video')

	def play_file(self, results, source={}, autoplay=False, background=False):
		def _resolve_dialog():
			self.url = None
			for count, item in enumerate(items, 1):
				try:
					self.caching_confirmed = False
					if not background:
						try:
							if self.progress_dialog.iscanceled(): break
							if kodi_utils.monitor.abortRequested() is True: break
							name = item['name'].replace('.', ' ').replace('-', ' ').upper()
							percent = int(count/float(total_items)*100)
							self.progress_dialog.update(line % ('', name, ''), percent)
						except: pass
					url = self.resolve_sources(item, self.meta)
					if url == 'uncached':
						url = _uncached_confirm(item)
						if url is None: return
					if url:
						self.url = url
						break
				except: pass
			self._kill_progress_dialog()
		def _uncached_confirm(item):
			if not kodi_utils.confirm_dialog(text=ls(32831) % item['debrid'].upper()):
				return None
			else:
				self.caching_confirmed = True
				return item
		try:
			self._kill_progress_dialog()
			if autoplay:
				items = [i for i in results if not 'Uncached' in i.get('cache_provider', '')]
				if self.filters_ignored: kodi_utils.notification(32686)
			else:
				results = [i for i in results if not 'Uncached' in i.get('cache_provider', '') or i == source]
				source_index = results.index(source)
				leading_index = max(source_index-20, 0)
				items_prev = results[leading_index:source_index]
				trailing_index = 41 - len(items_prev)
				items_next = results[source_index+1:source_index+trailing_index]
				items = [source] + items_next + items_prev
			total_items = len(items)
			line = '%s[CR]%s[CR]%s'
			if not background: self._make_progress_dialog()
			_resolve_dialog()
			if background: return self.url
			if self.caching_confirmed: return self.resolve_sources(self.url, self.meta, cache_item=True)
			return FenPlayer().run(self.url)
		except: pass

	def resolve_sources(self, item, meta, cache_item=False):
		try:
			if 'cache_provider' in item:
				cache_provider = item['cache_provider']
				if meta['vid_type'] == 'episode': title, season, episode = meta['ep_name'], meta['season'], meta['episode']
				else: title, season, episode = self._get_search_title(meta), None, None
				if cache_provider in ('Real-Debrid', 'Premiumize.me', 'AllDebrid'):
					url = resolver.resolve_cached_torrents(cache_provider, item['url'], item['hash'], title, season, episode)
					return url
				if 'Uncached' in cache_provider:
					if cache_item:
						if not 'package' in item: title, season, episode  = None, None, None
						url = resolver.resolve_uncached_torrents(item['debrid'], item['url'], item['hash'], title, season, episode)
						if not url: return None
						if url == 'cache_pack_success': return
						return FenPlayer().run(url)
					else:
						url = 'uncached'
						return url
					return None
			if item.get('scrape_provider', None) in default_internal_scrapers:
				url = resolver.resolve_internal_sources(item['scrape_provider'], item['id'], item['url_dl'], item.get('direct_debrid_link', False))
				return url
			if item.get('debrid') in ('Real-Debrid', 'Premiumize.me', 'AllDebrid') and not item['source'].lower() == 'torrent':
				url = resolver.resolve_debrid(item['debrid'], item['provider'], item['url'])
				if url is not None:
					return url
				else: return None
			else:
				url = item['url']
				return url
		except Exception: return
