# -*- coding: utf-8 -*-
"""
	Fenomscrapers Module
"""

from fenomscrapers.modules.control import addonPath, addonVersion, joinPath
from fenomscrapers.windows.textviewer import TextViewerXML
from fenomscrapers.modules import py_tools

if py_tools.isPY2:
	from io import open #py2 open() does not support encoding param

def get(file):
	fenomscrapers_path = addonPath()
	fenomscrapers_version = addonVersion()
	helpFile = joinPath(fenomscrapers_path, 'lib', 'fenomscrapers', 'help', file + '.txt')
	r = open(helpFile, 'r', encoding='utf-8', errors='ignore')
	text = r.read()
	r.close()
	heading = '[B]FenomScrapers -  v%s - %s[/B]' % (fenomscrapers_version, file)
	windows = TextViewerXML('textviewer.xml', fenomscrapers_path, heading=heading, text=text)
	windows.run()
	del windows