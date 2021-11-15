# -*- coding: utf-8 -*-
from sys import argv
try: from urllib import unquote
except ImportError: from urllib.parse import unquote
from caches.main_cache import main_cache
from modules import kodi_utils
# from modules.kodi_utils import logger

ls = kodi_utils.local_string
build_url = kodi_utils.build_url
make_listitem = kodi_utils.make_listitem
icon = kodi_utils.translate_path('special://home/addons/script.tikiart/resources/media/search.png')
fanart = kodi_utils.translate_path('special://home/addons/plugin.video.fen/fanart.png')

def search_history(params):
	def _builder():
		for h in history:
			try:
				cm = []
				name = unquote(h)
				url_params = {'mode': 'get_search_term', 'db_type': 'movie', 'query': name} if action == 'movie' \
						else {'mode': 'get_search_term', 'db_type': 'tv_show', 'query': name} if action == 'tvshow' \
						else {'mode': 'people_search.search', 'actor_name': name} if action == 'people' \
						else {'mode': 'furk.search_furk', 'db_type': 'video', 'query': name} if action == 'furk_video' \
						else {'mode': 'furk.search_furk', 'db_type': 'audio', 'music': True, 'query': name} if action == 'furk_audio' \
						else {'mode': 'easynews.search_easynews', 'query': name} if action == 'easynews_video' \
						else ''
				isFolder = False if action in ('movie', 'tvshow', 'people') else True
				display = '[B]%s %s : [/B]' % (display_title, sear_str) + name 
				url = build_url(url_params)
				cm.append((remove_str,'RunPlugin(%s)' % build_url({'mode': 'remove_from_history', 'setting_id':search_setting, 'name': name})))
				listitem = make_listitem()
				listitem.setLabel(display)
				listitem.setArt({'icon': icon, 'poster': icon, 'thumb': icon, 'fanart': fanart, 'banner': icon})
				listitem.addContextMenuItems(cm)
				yield (url, listitem, isFolder)
			except: pass
	try:
		__handle__ = int(argv[1])
		sear_str, mov_str, tv_str, peop_str = ls(32450).upper(), ls(32028).upper(), ls(32029).upper(), ls(32507).upper()
		furkvid_str = '%s %s' % (ls(32069).upper(), ls(32491).upper())
		furkaud_str = '%s %s' % (ls(32069).upper(), ls(32492).upper())
		remove_str, easy_str = ls(32786), ls(32070).upper()
		action = params['action']
		search_setting, display_title = {'movie': ('movie_queries', mov_str), 'tvshow': ('tvshow_queries', tv_str), 'people': ('people_queries', peop_str),
		'furk_video': ('furk_video_queries', furkvid_str), 'furk_audio': ('furk_audio_queries', furkaud_str), 'easynews_video': ('easynews_video_queries', easy_str)}[action]
		history = main_cache.get(search_setting)
		__handle__ = int(argv[1])
		kodi_utils.add_items(__handle__, list(_builder()))
	except: pass
	kodi_utils.set_content(__handle__, '')
	kodi_utils.end_directory(__handle__)
	kodi_utils.set_view_mode('view.main', '')
	