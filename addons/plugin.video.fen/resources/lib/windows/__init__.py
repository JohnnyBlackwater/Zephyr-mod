# -*- coding: utf-8 -*-
import xbmcgui
from modules.kodi_utils import execute_builtin, sleep, make_listitem, get_infolabel, player, build_url
from modules.utils import manual_function_import
from modules.settings import skin_location
# from modules.kodi_utils import logger

location = skin_location()

def create_window(import_info, skin_xml, **kwargs):
	'''
	import_info: tuple with ('module', 'function')
	'''
	try:
		function = manual_function_import(import_info[0], import_info[1])
		args = (skin_xml, location)
		window = function(*args, **kwargs)
		return window
	except Exception as e:
		from modules.kodi_utils import notification
		# from modules.kodi_utils import logger
		logger('error in open_window', str(e))
		return notification(32574)

def open_window(import_info, skin_xml, **kwargs):
	'''
	import_info: tuple with ('module', 'function')
	'''
	try:
		window = create_window(import_info, skin_xml, **kwargs)
		choice = window.run()
		del window
		return choice
	except: pass

class BaseDialog(xbmcgui.WindowXMLDialog):
	def __init__(self, *args):
		xbmcgui.WindowXMLDialog.__init__(self, args)
		self.closing_actions = [xbmcgui.ACTION_PARENT_DIR, xbmcgui.ACTION_PREVIOUS_MENU, xbmcgui.ACTION_STOP, xbmcgui.ACTION_NAV_BACK]
		self.selection_actions = [xbmcgui.ACTION_SELECT_ITEM, xbmcgui.ACTION_MOUSE_START]
		self.context_actions = [xbmcgui.ACTION_CONTEXT_MENU, xbmcgui.ACTION_MOUSE_RIGHT_CLICK, xbmcgui.ACTION_MOUSE_LONG_CLICK]
		self.info_actions = [xbmcgui.ACTION_SHOW_INFO]
		self.left_actions = [xbmcgui.ACTION_MOVE_LEFT]
		self.right_actions = [xbmcgui.ACTION_MOVE_RIGHT]
		self.up_actions = [xbmcgui.ACTION_MOVE_UP]
		self.down_actions = [xbmcgui.ACTION_MOVE_DOWN]
		self.player = player

	def make_listitem(self):
		return make_listitem()

	def build_url(self, params):
		return build_url(params)

	def execute_code(self, command):
		return execute_builtin(command)
	
	def get_position(self, window_id):
		return self.getControl(window_id).getSelectedPosition()

	def get_listitem(self, window_id):
		return self.getControl(window_id).getSelectedItem()

	def make_contextmenu_item(self, label, action, params):
		cm_item = self.make_listitem()
		cm_item.setProperty('tikiskins.context.label', label)
		cm_item.setProperty('tikiskins.context.action', action % self.build_url(params))
		return cm_item

	def get_infolabel(self, label):
		return get_infolabel(label)
	
	def open_window(self, import_info, skin_xml, **kwargs):
		return open_window(import_info, skin_xml, **kwargs)

	def sleep(self, time):
		sleep(time)

	def set_home_property(self, prop, value):
		xbmcgui.Window(10000).setProperty('fen.home_window.%s' % prop, value)

	def get_home_property(self, prop):
		return xbmcgui.Window(10000).getProperty('fen.home_window.%s' % prop)
