# -*- coding: utf-8 -*-
import os
import re
import json
try: from urlparse import urlparse
except ImportError: from urllib.parse import urlparse
try: from urllib import unquote, unquote_plus
except ImportError: from urllib.parse import unquote, unquote_plus
from fenomscrapers import pack_sources
from fenomscrapers.modules.control import getSettingDefault as fenom_default_settings, setting as fenom_getSetting, setSetting as fenom_setSetting
from modules import kodi_utils
from modules.utils import replace_html_codes
from modules.settings import date_offset
# from modules.kodi_utils import logger

source_folder_location = 'special://home/addons/script.module.fenomscrapers/lib/fenomscrapers/sources_fenomscrapers/%s'
source_subfolders = ('hosters', 'torrents')
source_path = 'fenomscrapers.sources_fenomscrapers.%s.%s'
string = str

RES_4K = ('.4k', 'hd4k', '4khd', '.uhd', 'ultrahd', 'ultra.hd', 'hd2160', '2160hd', '2160', '2160p', '216o', '216op')
RES_1080 = ('1080', '1080p', '1080i', 'hd1080', '1080hd', 'hd1080p', 'm1080p', 'fullhd', 'full.hd', '1o8o', '1o8op', '108o', '108op', '1o80', '1o80p')
RES_720 = ('720', '720p', '720i', 'hd720', '720hd', 'hd720p', 'hd', '72o', '72op')
CAM = ('.cam.', 'camrip', 'hdcam', '.hd.cam', 'cam.rip', 'dvdcam')
SCR = ('.scr', 'screener', 'dvdscr', 'dvd.scr', '.r5', '.r6')
TELE = ('.tc.', 'tsrip', 'hdts', 'hdtc', '.hd.tc', 'dvdts', 'telesync', '.ts.')
VIDEO_3D = ('.3d.', '.sbs.', '.hsbs', 'sidebyside', 'side.by.side', 'stereoscopic', '.tab.', '.htab.', 'topandbottom', 'top.and.bottom')
DOLBY_VISION = ('dolby.vision', 'dolbyvision', '.dovi.', '.dv.')
HDR = ('2160p.uhd.bluray', '2160p.uhd.blu.ray', '2160p.bluray.hevc.truehd', '2160p.blu.ray.hevc.truehd',
			'2160p.bluray.hevc.dts.hd.ma', '2160p.blu.ray.hevc.dts.hd.ma', '.hdr.', 'hdr10', 'hdr.10',
			'uhd.bluray.2160p', 'uhd.blu.ray.2160p')
CODEC_H264 = ('avc', 'h264', 'h.264', 'x264', 'x.264')
CODEC_H265 = ('h265', 'h.265', 'hevc', 'x265', 'x.265')
CODEC_XVID = ('xvid', '.x.vid')
CODEC_DIVX = ('divx', 'div2', 'div3', 'div4')
CODEC_MPEG = ('.mpg', '.mp2', '.mpeg', '.mpe', '.mpv', '.mp4', '.m4p', '.m4v', 'msmpeg', 'mpegurl')
CODEC_MKV = ('.mkv', 'matroska')
REMUX = ('remux', 'bdremux')
BLURAY = ('bluray', 'blu.ray', 'bdrip', 'bd.rip')
DVD = ('dvdrip', 'dvd.rip')
WEB = ('.web.', 'webdl', 'web.dl', 'web-dl', 'webrip', 'web.rip')
HDRIP = ('.hdrip', '.hd.rip')
DOLBY_TRUEHD = ('true.hd', 'truehd')
DOLBY_DIGITALPLUS = ('dolby.digital.plus', 'dolbydigital.plus', 'dolbydigitalplus', 'dd.plus.', 'ddplus', '.ddp.', 'ddp2', 'ddp5', 'ddp7', 'eac3', '.e.ac3')
DOLBY_DIGITALEX = ('.dd.ex.', 'ddex', 'dolby.ex.', 'dolby.digital.ex.', 'dolbydigital.ex.')
DOLBYDIGITAL = ('dd2.', 'dd5', 'dd7', 'dolby.digital', 'dolbydigital', '.ac3', '.ac.3.', '.dd.')
DTSX = ('dts.x.', 'dtsx')
DTS_HDMA = ('hd.ma', 'hdma')
DTS_HD = ('dts.hd.', 'dtshd')
AUDIO_8CH = ('ch8.', '8ch.', '7.1ch', '7.1.')
AUDIO_7CH = ('ch7.', '7ch.', '6.1ch', '6.1.')
AUDIO_6CH = ('ch6.', '6ch.', '5.1ch', '5.1.')
AUDIO_2CH = ('ch2', '2ch', '2.0ch', '2.0.', 'audio.2.0.', 'stereo')
MULTI_LANG = ('hindi.eng', 'ara.eng', 'ces.eng', 'chi.eng', 'cze.eng', 'dan.eng', 'dut.eng', 'ell.eng', 'esl.eng', 'esp.eng', 'fin.eng', 'fra.eng', 'fre.eng',
				'frn.eng', 'gai.eng', 'ger.eng', 'gle.eng', 'gre.eng', 'gtm.eng', 'heb.eng', 'hin.eng', 'hun.eng', 'ind.eng', 'iri.eng', 'ita.eng', 'jap.eng', 'jpn.eng',
				'kor.eng', 'lat.eng', 'lebb.eng', 'lit.eng', 'nor.eng', 'pol.eng', 'por.eng', 'rus.eng', 'som.eng', 'spa.eng', 'sve.eng', 'swe.eng', 'tha.eng', 'tur.eng',
				'uae.eng', 'ukr.eng', 'vie.eng', 'zho.eng', 'dual.audio', 'multi')
SUBS = ('subita', 'subfrench', 'subspanish', 'subtitula', 'swesub', 'nl.subs')
ADS = ('1xbet', 'betwin')

unwanted_tags = ('tamilrockers.com', 'www.tamilrockers.com', 'www.tamilrockers.ws', 'www.tamilrockers.pl', 'www.tamilrockerrs.pl',
			'www.torrenting.com', 'www.torrenting.org', 'www-torrenting-com', 'www-torrenting-org',
			'+katmoviehd.pw+', 'katmoviehd-pw',
			'www.torrent9.nz', 'torrent9-cz-.-', 'torrent9.cz.].', 'torrent9-cz-]-',
			'agusiq-torrents-pl', 'oxtorrent-com',
			'www.movcr.tv', 'movcr-com', 'www.movcr.to',
			'(imax)', '.imax.',
			'xtorrenty.org', 'nastoletni.wilkoak', 'www.scenetime.com', 'kst-vn',
			'www.2movierulz.ac', 'www.2movierulz.ms',
			'www.3movierulz.com', 'www.3movierulz.tv', 'www.3movierulz.ws', 'www.3movierulz.ms', 'www.8movierulz.ws',
			'mkvcinemas.live',
			'www.bludv.tv', 'ramin.djawadi', 'extramovies.casa',
			'+13.+', 'taht.oyunlar', 'crazy4tv.com', 'karibu', '989pa.com',
			'best-torrents-net', '1-3-3-8.com', 'ssrmovies.club', 'www.tamilmv.bid', 'www.1tamilmv.org',
			'va:', 'oxtorrent-sh', 'zgxybbs-fdns-uk', 'www.tamilblasters.mx',
			'www.1tamilmv.work', 'www.7movierulz.pw', 'www.xbay.me', 'www-tamilrockers-cl', 'www.tamilrockers.cl', 'www.tamilrockers.li',
			'crazy4tv-com', '(es)', 'cls', 'usabiit.com')

def sources(ignore_disabled):
	def import_info():
		for item in source_subfolders:
			files = kodi_utils.list_dirs(kodi_utils.translate_path(source_folder_location % item))[1]
			for m in files:
				try:
					m_split = m.split('.')
					if m_split[1] == 'pyo': continue
					module_name = m_split[0]
					if module_name == '__init__': continue
					if not ignore_disabled and not enabled_scraper(module_name): continue
					module_path = source_path % (item, module_name)
					yield (module_name, module_path, '')
				except: pass
	try: sourceDict = list(import_info())
	except: sourceDict = []
	return sourceDict

def enabled_scraper(module_name):
	return fenom_getSetting('provider.%s' % module_name) == 'true'

def get_pack_sources():
	return pack_sources()

def get_aliases_titles(aliases):
	try: result = [i['title'] for i in aliases]
	except: result = []
	return result

def internal_results(provider, sources):
	kodi_utils.window.setProperty('%s.internal_results' % provider, json.dumps(sources))

def normalize(title):
	try:
		try: return title.decode('ascii').encode('utf-8')
		except: pass
		try: import unicodedata
		except ImportError: return
		title = u'%s' % obj
		title = ''.join(c for c in unicodedata.normalize('NFD', title) if unicodedata.category(c) != 'Mn')
		return string(title)
	except:
		return title

def _ext_scrapers_notice(status):
	kodi_utils.notification(status, 2500)

def toggle_all(folder, setting, silent=False):
	try:
		sourcelist = scraper_names(folder)
		for i in sourcelist:
			source_setting = 'provider.' + i
			fenom_setSetting(source_setting, setting)
		if silent: return
		return _ext_scrapers_notice(32576)
	except:
		if silent: return
		return _ext_scrapers_notice(32574)

def enable_disable_specific_all(folder):
	try:
		icon = kodi_utils.ext_addon('script.module.fenomscrapers').getAddonInfo('icon')
		enabled, disabled = scrapers_status(folder)
		all_sources = sorted(enabled + disabled)
		preselect = [all_sources.index(i) for i in enabled]
		list_items = [{'line1': i.upper(), 'icon': icon} for i in all_sources]
		kwargs = {'items': json.dumps(list_items), 'heading': 'Fen', 'enumerate': 'false', 'multi_choice': 'true', 'multi_line': 'false', 'preselect': preselect}
		chosen = kodi_utils.select_dialog(all_sources, **kwargs)
		if chosen == None: return
		for i in all_sources:
			if i in chosen: fenom_setSetting('provider.' + i, 'true')
			else: fenom_setSetting('provider.' + i, 'false')
		return _ext_scrapers_notice(32576)
	except: return _ext_scrapers_notice(32574)

def set_default_scrapers():
	all_scrapers = scraper_names('all')
	for i in all_scrapers:
		scraper = 'provider.' + i
		default_setting = fenom_default_settings(scraper)
		fenom_setSetting(scraper, default_setting)

def scrapers_status(folder='all'):
	providers = scraper_names(folder)
	enabled = [i for i in providers if fenom_getSetting('provider.' + i) == 'true']
	disabled = [i for i in providers if i not in enabled]
	return enabled, disabled

def scraper_names(folder):
	providerList = []
	append = providerList.append
	sourceSubFolders = ['hosters', 'torrents']
	if folder != 'all':
		sourceSubFolders = [i for i in sourceSubFolders if i == folder]
	for item in sourceSubFolders:
		files = kodi_utils.list_dirs(kodi_utils.translate_path(source_folder_location % item))[1]
		for m in files:
			if not os.path.splitext(urlparse(m).path)[-1] == '.py':
				continue
			module_name = m.split('.')[0]
			if module_name == '__init__':
				continue
			append(module_name)
	return providerList

def pack_enable_check(meta, season, episode):
	extra_info = meta['extra_info']
	status = extra_info['status'].lower()
	if status in ('ended', 'canceled'): return True, True
	from metadata import season_episodes_meta, retrieve_user_info
	from modules.utils import adjust_premiered_date, get_datetime
	adjust_hours = date_offset()
	current_date = get_datetime()
	meta_user_info = retrieve_user_info(kodi_utils.window)
	episodes_data = season_episodes_meta(season, meta, meta_user_info)
	unaired_episodes = [adjust_premiered_date(i['premiered'], adjust_hours)[0] for i in episodes_data]
	if None in unaired_episodes or any(i > current_date for i in unaired_episodes): return False, False
	else: return True, False
	return False, False

def get_filename_match(title, url, name=None):
	from modules.utils import clean_file_name
	if name: return clean_file_name(name)
	from modules.utils import clean_title, normalize
	title_match = None
	try:
		title = clean_title(normalize(title))
		name_url = unquote(url)
		try: file_name = clean_title(name_url.split('/')[-1])
		except: return title_match
		test = name_url.split('/')
		for item in test:
			test_url = string(clean_title(normalize(item)))
			if title in test_url:
				title_match = clean_file_name(string(item)).replace('html', ' ').replace('+', ' ')
				break
	except:
		pass
	return title_match

def clear_scrapers_cache(silent=False):
	from modules.nav_utils import clear_cache
	for item in ('internal_scrapers', 'external_scrapers'): clear_cache(item, silent=True)
	if not silent: kodi_utils.notification(32576)

def clear_and_rescrape(content, meta, season=None, episode=None):
	from caches.providers_cache import providerCache
	from modules.sources import Sources
	from modules.nav_utils import clear_cache
	kodi_utils.show_busy_dialog()
	deleted = providerCache.delete_cache_single(content, meta['tmdb_id'])
	if not deleted: return kodi_utils.notification(32574)
	for item in ('internal_scrapers', 'external_scrapers'): clear_cache(item, silent=True)
	if content in ('movie', 'movies'):
		play_params = {'mode': 'play_media', 'vid_type': 'movie', 'tmdb_id': meta['tmdb_id'], 'autoplay': 'False'}
	else:
		play_params = {'mode': 'play_media', 'vid_type': 'episode', 'tmdb_id': meta['tmdb_id'],
					'tvshowtitle': meta['rootname'], 'season': season, 'episode': episode, 'autoplay': 'False'}
	kodi_utils.hide_busy_dialog()
	Sources().playback_prep(play_params)

def rescrape_with_disabled(content, meta, season=None, episode=None):
	from modules.sources import Sources
	try: meta = json.loads(meta)
	except: pass
	if content in ('movie', 'movies'):
		play_params = {'mode': 'play_media', 'vid_type': 'movie', 'tmdb_id': meta['tmdb_id'],
						'autoplay': 'False', 'disabled_ignored': 'true', 'prescrape': 'false'}
	else:
		play_params = {'mode': 'play_media', 'vid_type': 'episode', 'tmdb_id': meta['tmdb_id'], 'tvshowtitle': meta['rootname'], 'season': season,
						'episode': episode, 'autoplay': 'False', 'disabled_ignored': 'true', 'prescrape': 'false'}
	Sources().playback_prep(play_params)

def scrape_with_custom_values(content, meta, season=None, episode=None):
	from windows import open_window
	from modules.sources import Sources
	ls = kodi_utils.local_string
	try: meta = json.loads(meta)
	except: pass
	if content in ('movie', 'movies'):
		play_params = {'mode': 'play_media', 'vid_type': 'movie', 'tmdb_id': meta['tmdb_id'],
						'autoplay': 'False', 'prescrape': 'false'}
	else:
		play_params = {'mode': 'play_media', 'vid_type': 'episode', 'tmdb_id': meta['tmdb_id'], 'tvshowtitle': meta['rootname'], 'season': season,
						'episode': episode, 'autoplay': 'False', 'prescrape': 'false'}
	custom_title = kodi_utils.dialog.input(ls(32228), defaultt=meta['title'])
	if not custom_title: return
	play_params['custom_title'] = custom_title
	if content in ('movie', 'movies'):
		custom_year = kodi_utils.dialog.input('%s (%s)' % (ls(32543), ls(32669)), type=kodi_utils.numeric_input, defaultt=str(meta['year']))
		if custom_year: play_params['custom_year'] = int(custom_year)
	choice = open_window(('windows.yes_no_progress_media', 'YesNoProgressMedia'), 'yes_no_progress_media.xml',
							meta=meta, enable_buttons='playmode_status', resume_dialog='%s?' % ls(32006), percent=0)
	if choice == True: play_params['disabled_ignored'] = 'true'
	elif choice == None: return
	Sources().playback_prep(play_params)

def supported_video_extensions():
	supported_video_extensions = kodi_utils.supported_media().split('|')
	return [i for i in supported_video_extensions if not i in ('','.zip')]

def seas_ep_query_list(season, episode):
	season = int(season)
	episode = int(episode)
	return ['s%de%02d' % (int(season), int(episode)),
			's%02de%02d' % (int(season), int(episode)),
			'%dx%02d' % (int(season), int(episode)),
			'%02dx%02d' % (int(season), int(episode)),
			'season%02depisode%02d' % (int(season), int(episode)),
			'season%depisode%02d' % (int(season), int(episode)),
			'season%depisode%d' % (int(season), int(episode))]

def seas_ep_filter(season, episode, release_title, split=False, return_match=False):
	string_list = []
	str_season = string(season)
	str_episode = string(episode)
	str_ep_plus_1 = string(episode+1)
	str_ep_minus_1 = string(episode-1)
	append = string_list.append
	release_title = re.sub(r'[^A-Za-z0-9-]+', '.', unquote(release_title).replace('\'', '')).lower()
	string1 = r'(s<<S>>e<<E>>)|' \
			  r'(s<<S>>\.e<<E>>)|' \
			  r'(s<<S>>ep<<E>>)|' \
			  r'(s<<S>>\.ep<<E>>)'
	string2 = r'(season\.<<S>>\.episode\.<<E>>)|' \
			  r'(season<<S>>\.episode<<E>>)|' \
			  r'(season<<S>>episode<<E>>)|' \
			  r'(<<S>>x<<E>>\.)|' \
			  r'(s<<S>>e\(<<E>>\))|' \
			  r'(s<<S>>\.e\(<<E>>\))|' \
			  r'(<<S>>\.<<E>>\.)'
	string3 = r'(<<S>><<E>>\.)'
	string4 = r'(s<<S>>e<<E1>>e<<E2>>)|' \
			  r'(s<<S>>e<<E1>>-e<<E2>>)|' \
			  r'(s<<S>>e<<E1>>\.e<<E2>>)|' \
			  r'(s<<S>>e<<E1>>-<<E2>>)-|' \
			  r'(s<<S>>e<<E1>>\.<<E2>>)\.|' \
			  r'(s<<S>>e<<E1>><<E2>>)'
	# string5 = r'(?<![a-z])(ep<<E>>[.-])|' \
	# 		  r'(?<![a-z])e<<E>>[.-]|' \
	# 		  r'(?<![a-z])(ep[.-]<<E>>[.-])'
	append(string1.replace('<<S>>', str_season.zfill(2)).replace('<<E>>', str_episode.zfill(2)))
	append(string1.replace('<<S>>', str_season).replace('<<E>>', str_episode.zfill(2)))
	append(string2.replace('<<S>>', str_season.zfill(2)).replace('<<E>>', str_episode.zfill(2)))
	append(string2.replace('<<S>>', str_season).replace('<<E>>', str_episode.zfill(2)))
	append(string2.replace('<<S>>', str_season.zfill(2)).replace('<<E>>', str_episode))	
	append(string2.replace('<<S>>', str_season).replace('<<E>>', str_episode))
	append(string3.replace('<<S>>', str_season.zfill(2)).replace('<<E>>', str_episode.zfill(2)))
	append(string3.replace('<<S>>', str_season).replace('<<E>>', str_episode.zfill(2)))
	append(string4.replace('<<S>>', str_season.zfill(2)).replace('<<E1>>', str_ep_minus_1.zfill(2)).replace('<<E2>>', str_episode.zfill(2)))
	append(string4.replace('<<S>>', str_season.zfill(2)).replace('<<E1>>', str_episode.zfill(2)).replace('<<E2>>', str_ep_plus_1.zfill(2)))
	# append(string5.replace('<<E>>', str_episode.zfill(2)))
	final_string = '|'.join(string_list)
	reg_pattern = re.compile(final_string)
	if split: return release_title.split(re.search(reg_pattern, release_title).group(), 1)[1]
	elif return_match: return re.search(reg_pattern, release_title).group()
	else: return bool(re.search(reg_pattern, release_title))

def extras_filter():
	return ['sample', 'extra', 'extras', 'deleted', 'unused', 'footage', 'inside', 'blooper', 'bloopers', 'making.of', 'feature', 'featurette', 'behind.the.scenes', 'trailer']

def find_season_in_release_title(release_title):
	release_title = re.sub(r'[^A-Za-z0-9-]+', '.', unquote(release_title).replace('\'', '')).lower()
	match = None
	regex_list = [r's(\d+)', r's\.(\d+)', r'(\d+)x', r'(\d+)\.x', r'season(\d+)', r'season\.(\d+)']
	for item in regex_list:
		try:
			match = re.search(item, release_title)
			if match:
				match = int(string(match.group(1)).lstrip('0'))
				break
		except: pass
	return match

def check_title(title, release_title, aliases, year, season, episode):
	try:
		all_titles = [title]
		if aliases: all_titles += aliases
		cleaned_titles = []
		append = cleaned_titles.append
		year = string(year)
		for i in all_titles: append(i.lower().replace(':', '').replace('!', '').replace('(', '').replace(')', '').replace('&', 'and').replace(' ', '.').replace(year, ''))
		release_title = strip_non_ascii_and_unprintable(release_title).lstrip('/ ').replace(' ', '.').replace(':', '.').lower()
		releasetitle_startswith = release_title.lower().startswith
		for i in unwanted_tags:
			if releasetitle_startswith(i):
				i_startswith = i.startswith
				pattern = r'\%s' % i if i_startswith('[') or i_startswith('+') else r'%s' % i
				release_title = re.sub(r'^%s' % pattern, '', release_title, 1, re.I)
		release_title = release_title.lstrip('.-:/')
		release_title = re.sub(r'^\[.*?]', '', release_title, 1, re.I)
		release_title = release_title.lstrip('.-[](){}:/')
		if season:
			try: hdlr = seas_ep_filter(season, episode, release_title, return_match=True)
			except: return False
		else: hdlr = year
		release_title = release_title.split(hdlr.lower())[0].replace(year, '').replace('(', '').replace(')', '').replace('&', 'and').rstrip('.-').rstrip('.').rstrip('-').replace(':', '')
		if not any(release_title == i for i in cleaned_titles): return False
		return True
	except: return True

def strip_non_ascii_and_unprintable(text):
	try:
		result = ''.join(char for char in text if char in printable)
		return result.encode('ascii', errors='ignore').decode('ascii', errors='ignore')
	except:
		from fenomscrapers.modules import log_utils
		log_utils.error()
		return text

def release_info_format(release_title):
	try:
		release_title = url_strip(release_title)
		release_title = release_title.lower().replace("'", "").lstrip('.').rstrip('.')
		fmt = '.%s.' % re.sub(r'[^a-z0-9-~]+', '.', release_title).replace('.-.', '.').replace('-.', '.').replace('.-', '.').replace('--', '.')
		return fmt
	except:
		return release_title.lower()

def clean_title(title):
	try:
		if not title: return
		title = title.lower()
		title = re.sub(r'&#(\d+);', '', title)
		title = re.sub(r'(&#[0-9]+)([^;^0-9]+)', '\\1;\\2', title)
		title = re.sub(r'(&#[0-9]+)([^;^0-9]+)', '\\1;\\2', title)
		title = title.replace('&quot;', '\"').replace('&amp;', '&')
		title = re.sub(r'\n|([\[({].+?[})\]])|([:;–\-"\',!_.?~$@])|\s', '', title)
	except: pass
	return title

def get_release_quality(release_info):
	if any(i in release_info for i in SCR): return 'SCR'
	elif any(i in release_info for i in CAM): return 'CAM'
	elif any(i in release_info for i in TELE): return 'TELE'
	elif any(i in release_info for i in RES_4K): return '4K'
	elif any(i in release_info for i in RES_1080): return '1080p'
	elif any(i in release_info for i in RES_720): return '720p'
	else: return 'SD'

def url_strip(url):
	try:
		url = unquote_plus(url)
		if 'magnet:' in url: url = url.split('&dn=')[1]
		url = url.lower().replace("'", "").lstrip('.').rstrip('.')
		fmt = re.sub(r'[^a-z0-9]+', ' ', url)
		if 'http' in fmt: return None
		if fmt == '': return None
		else: return fmt
	except: return None

def get_file_info(name_info=None, url=None):
	# thanks Venom 123. :)
	info = ''
	if name_info: fmt = name_info
	elif url: fmt = url_strip(url)
	if not fmt: return info
	quality = get_release_quality(fmt)
	if any(value in fmt for value in VIDEO_3D):  info += ' [B]3D[/B] |'
	if '.sdr' in fmt: info += ' SDR |'
	elif any(value in fmt for value in DOLBY_VISION): info += ' [B]D/VISION[/B] |'
	elif any(value in fmt for value in HDR): info += ' [B]HDR[/B] |'
	elif all(i in fmt for i in ('2160p', 'remux')): info += ' [B]HDR[/B] |'
	if any(value in fmt for value in CODEC_H264): info += ' AVC |'
	elif any(value in fmt for value in CODEC_H265): info += ' [B]HEVC[/B] |'
	elif any(i in info for i in (' [B]HDR[/B] ', ' [B]D/VISION[/B] ')): info += ' [B]HEVC[/B] |'
	elif any(value in fmt for value in CODEC_XVID): info += ' XVID |'
	elif any(value in fmt for value in CODEC_DIVX): info += ' DIVX |'
	if any(value in fmt for value in REMUX): info += ' REMUX |'
	if any(value in fmt for value in BLURAY): info += ' BLURAY |'
	elif any(i in fmt for i in DVD): info += ' DVD |'
	elif any(value in fmt for value in WEB): info += ' WEB |'
	elif 'hdtv' in fmt: info += ' HDTV |'
	elif 'pdtv' in fmt: info += ' PDTV |'
	elif any(value in fmt for value in HDRIP): info += ' HDRIP |'
	if 'atmos' in fmt: info += ' ATMOS |'
	if any(value in fmt for value in DOLBY_TRUEHD): info += ' TRUEHD |'
	if any(value in fmt for value in DOLBY_DIGITALPLUS): info += ' DD+ |'
	elif any(value in fmt for value in DOLBY_DIGITALEX): info += ' DD-EX |'
	elif any(value in fmt for value in DOLBYDIGITAL): info += ' DD |'
	if 'aac' in fmt: info += ' AAC |'
	elif 'mp3' in fmt: info += ' MP3 |'
	if any(value in fmt for value in DTSX): info += ' DTS-X |'
	elif any(value in fmt for value in DTS_HDMA): info += ' DTS-HD MA |'
	elif any(value in fmt for value in DTS_HD): info += ' DTS-HD |'
	elif '.dts' in fmt: info += ' DTS |'
	if any(value in fmt for value in AUDIO_8CH): info += ' 8CH |'
	elif any(value in fmt for value in AUDIO_7CH): info += ' 7CH |'
	elif any(value in fmt for value in AUDIO_6CH): info += ' 6CH |'
	elif any(value in fmt for value in AUDIO_2CH): info += ' 2CH |'
	if '.wmv' in fmt: info += ' WMV |'
	elif any(value in fmt for value in CODEC_MPEG): info += ' MPEG |'
	elif '.avi' in fmt: info += ' AVI |'
	elif any(value in fmt for value in CODEC_MKV): info += ' MKV |'
	if any(value in fmt for value in MULTI_LANG): info += ' MULTI-LANG |'
	if any(value in fmt for value in ADS): info += ' ADS |'
	if any(value in fmt for value in SUBS):
		if info != '': info += ' SUBS'
		else: info = 'SUBS'
	info = info.rstrip('|')
	return quality, info




