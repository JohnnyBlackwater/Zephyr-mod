# -*- coding: utf-8 -*-
import os
import time
import datetime
import xml.etree.ElementTree as ET
from windows import open_window
from caches import check_databases, clean_databases
from apis.trakt_api import trakt_sync_activities
from modules import kodi_utils
from modules import settings
from modules.nav_utils import sync_MyAccounts
from modules.utils import gen_file_hash
from modules.settings_reader import get_setting, set_setting, make_settings_dict
from modules.kodi_utils import logger

ls = kodi_utils.local_string
addon_dir = kodi_utils.translate_path('special://home/addons/plugin.video.fen')
db_types = ['movie', 'tvshow']

class InitializeDatabases:
	def run(self):
		logger('FEN', 'InitializeDatabases Service Starting')
		try: check_databases()
		except: pass
		return logger('FEN', 'InitializeDatabases Service Finished')

class CheckSettingsFile:
	def run(self):
		logger('FEN', 'CheckSettingsFile Service Starting')
		kodi_utils.window.clearProperty('fen_settings')
		profile_dir = kodi_utils.translate_path('special://profile/addon_data/plugin.video.fen/')
		if not kodi_utils.path_exists(profile_dir): kodi_utils.make_directorys(profile_dir)
		settings_xml = os.path.join(profile_dir, 'settings.xml')
		if not kodi_utils.path_exists(settings_xml):
			__addon__ = kodi_utils.addon()
			addon_version = __addon__.getAddonInfo('version')
			__addon__.setSetting('version_number', addon_version)
			kodi_utils.monitor.waitForAbort(0.5)
		make_settings_dict()
		return logger('FEN', 'CheckSettingsFile Service Finished')

class SyncMyAccounts:
	def run(self):
		logger('FEN', 'SyncMyAccounts Service Starting')
		sync_MyAccounts(silent=True)
		return logger('FEN', 'SyncMyAccounts Service Finished')

class ClearSubs:
	def run(self):
		logger('FEN', 'Clear Subtitles Service Starting')
		subtitle_path = kodi_utils.translate_path('special://temp/')
		files = kodi_utils.list_dirs(subtitle_path)[1]
		for i in files:
			try:
				if i.startswith('FENSubs_'): kodi_utils.delete_file(os.path.join(subtitle_path, i))
				if i.endswith('.nfo'): kodi_utils.delete_file(os.path.join(subtitle_path, i))
			except: pass
		return logger('FEN', 'Clear Subtitles Service Finished')

class ReuseLanguageInvokerCheck:
	def run(self):
		logger('FEN', 'ReuseLanguageInvokerCheck Service Starting')
		if kodi_utils.get_kodi_version() < 18: return
		addon_xml = os.path.join(addon_dir, 'addon.xml')
		tree = ET.parse(addon_xml)
		root = tree.getroot()
		current_addon_setting = get_setting('reuse_language_invoker', 'true')
		try: current_xml_setting = [str(i.text) for i in root.iter('reuselanguageinvoker')][0]
		except: return logger('FEN', 'ReuseLanguageInvokerCheck Service Finished')
		if current_xml_setting == current_addon_setting:
			return logger('FEN', 'ReuseLanguageInvokerCheck Service Finished')
		for item in root.iter('reuselanguageinvoker'):
			item.text = current_addon_setting
			hash_start = gen_file_hash(addon_xml)
			tree.write(addon_xml)
			hash_end = gen_file_hash(addon_xml)
			logger('FEN', 'ReuseLanguageInvokerCheck Service Finished')
			if hash_start != hash_end:
				if not kodi_utils.confirm_dialog(text='%s\n%s' % (ls(33021), ls(33020))): return
				current_profile = kodi_utils.get_infolabel('system.profilename')
				kodi_utils.execute_builtin('LoadProfile(%s)' % current_profile)
			else: kodi_utils.ok_dialog(text=32574, top_space=True)

class ViewsSetWindowProperties:
	def run(self):
		logger('FEN', 'ViewsSetWindowProperties Service Starting')
		try: kodi_utils.set_view_properties()
		except: pass
		return logger('FEN', 'ViewsSetWindowProperties Service Finished')

class ShowChangelog:
	def run(self):
		logger('FEN', 'ShowChangelog Service Starting')
		addon_version = kodi_utils.addon().getAddonInfo('version')
		setting_version = get_setting('version_number')
		if addon_version != setting_version:
			set_setting('version_number', addon_version)
			kodi_utils.window.setProperty('fen_display_changelog', 'true')
		else: kodi_utils.window.setProperty('fen_display_changelog', 'false')
		return logger('FEN', 'ShowChangelog Service Finished')

class AutoRun:
	def run(self):
		try:
			logger('FEN', 'AutoRun Service Starting')
			if settings.auto_start_fen(): kodi_utils.execute_builtin('RunAddon(plugin.video.fen)')
			logger('FEN', 'AutoRun Service Finished')
			return
		except: return

class DatabaseMaintenance:
	def run(self):
		self.time = datetime.datetime.now()
		current_time = self._get_timestamp(self.time)
		due_clean = int(get_setting('database.maintenance.due', '0'))
		if current_time >= due_clean:
			logger('FEN', 'Database Maintenance Service Starting')
			kodi_utils.monitor.waitForAbort(10.0)
			try: clean_databases(current_time, database_check=False, silent=True)
			except: pass
			next_clean = str(int(self._get_timestamp(self.time + datetime.timedelta(days=3))))
			set_setting('database.maintenance.due', next_clean)
			return logger('FEN', 'Database Maintenance Service Finished')

	def _get_timestamp(self, date_time):
		return int(time.mktime(date_time.timetuple()))

class TraktMonitor:
	def run(self):
		logger('FEN', 'TraktMonitor Service Starting')
		trakt_service_string = 'TraktMonitor Service Update %s - %s'
		update_string = 'Next Update in %s minutes...'
		kodi_utils.window.setProperty('fen_traktsync_firstrun', 'true')
		while not kodi_utils.monitor.abortRequested():
			while kodi_utils.player.isPlaying() or kodi_utils.get_visibility('Library.IsScanningVideo') or kodi_utils.get_visibility('System.ScreenSaverActive'):
				kodi_utils.monitor.waitForAbort(10)
			value, interval = settings.trakt_sync_interval()
			next_update_string = update_string % value
			status = trakt_sync_activities()
			if status == 'success':
				if settings.trakt_sync_refresh_widgets():
					if kodi_utils.window.getProperty('fen_traktsync_firstrun') == 'true':
						logger('FEN', trakt_service_string % ('Widgets Refresh', 'Setting Activated. Skipped Refresh for First Run'))
					else:
						kodi_utils.execute_builtin('UpdateLibrary(video,special://skin/foo)')
						logger('FEN', trakt_service_string % ('Widgets Refresh', 'Setting Activated. Refresh Performed'))
				else:
					logger('FEN', trakt_service_string % ('Widgets Refresh', 'Setting Disabled. Skipping Refresh'))
			elif status == 'no account':
				logger('FEN', trakt_service_string % ('Aborted. No Trakt Account Active', next_update_string))
			elif status == 'failed':
				logger('FEN', trakt_service_string % ('Failed. Error from Trakt', next_update_string))
			else:# 'not needed'
				logger('FEN', trakt_service_string % ('Success. No Changes Needed', next_update_string))
			kodi_utils.window.setProperty('fen_traktsync_firstrun', 'false')
			kodi_utils.monitor.waitForAbort(interval)
		return logger('FEN', 'TraktMonitor Service Finished')
