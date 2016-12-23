import sublime, sublime_plugin
import os
import re

def md(*t):
	t = ' '.join([str(el) for el in t])
	sublime.message_dialog(t)

def sm(*t):
	t = ' '.join([str(el) for el in t])
	sublime.status_message(t)

def em(*t):
	t = ' '.join([str(el) for el in t])
	sublime.error_message(t)

class FileInfoCommand(sublime_plugin.TextCommand):



	def run(self, edit, *args, **kwargs):
		self.window = self.view.window()
		self.selection = sublime.Selection(self.view.id())
		self.settings = self.view.settings()

		info = []
		info.append(self.view.file_name() or 'Untitled')
		info.append(self.view.size())
		text = []
		text.append('Name: ' + (self.view.file_name() or 'Untitled'))
		text.append('Char: ' + str(self.view.size()))
		arr = re.split( '[' + re.escape( self.settings.get('word_separators') ) + '\n]', self.view.substr( sublime.Region(0, self.view.size()) ) )
		while '' in arr:
			arr.remove('')

		text.append('Word: ' + str( len(arr ) ) )
		text = '\n'.join(text)
		md(text)