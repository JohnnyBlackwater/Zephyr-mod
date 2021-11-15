# -*- coding: utf-8 -*-
import json
from modules.kodi_utils import addon, get_kodi_version, translate_path, window, path_exists, make_directorys
# from modules.kodi_utils import logger

def set_setting(setting_id, value):
	addon().setSetting(setting_id, value)

def get_setting(setting_id, fallback=None):
	try: settings_dict = json.loads(window.getProperty('fen_settings'))
	except: settings_dict = make_settings_dict()
	if settings_dict is None: settings_dict = get_setting_fallback(setting_id)
	value = settings_dict.get(setting_id, '')
	if fallback is None: return value
	if value == '': return fallback
	return value

def get_setting_fallback(setting_id):
	return {setting_id: addon().getSetting(setting_id)}

def make_settings_dict():
	import xml.etree.ElementTree as ET
	settings_dict = None
	try:
		kodi_version = get_kodi_version()
		test_path = translate_path('special://profile/addon_data/plugin.video.fen/')
		profile_dir = 'special://profile/addon_data/plugin.video.fen/%s'
		if not path_exists(test_path): make_directorys(test_path)
		settings_xml = translate_path(profile_dir % 'settings.xml')
		root = ET.parse(settings_xml).getroot()
		settings_dict = {}
		for item in root:
			setting_id = item.get('id')
			if kodi_version >= 18: setting_value = item.text
			else: setting_value = item.get('value')
			if setting_value is None: setting_value = ''
			dict_item = {setting_id: setting_value}
			settings_dict.update(dict_item)
		window.setProperty('fen_settings', json.dumps(settings_dict))
	except: pass
	return settings_dict
