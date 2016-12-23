import sublime, sublime_plugin
import os

def md(*t):
	t = ' '.join([str(el) for el in t])
	sublime.message_dialog(t)

def sm(*t):
	t = ' '.join([str(el) for el in t])
	sublime.status_message(t)

def em(*t):
	t = ' '.join([str(el) for el in t])
	sublime.error_message(t)

class SublimeCommandRunnerCommand(sublime_plugin.TextCommand):

	def get_setting(self, name):
		return sublime.load_settings('Preferences.sublime-settings').get(name) or \
		sublime.load_settings('snippet-saver.sublime-settings').get(name)
	
	def on_done(self, text):
		text = text.split(' ')
		for t in text:
			if t == 'cmd1':
				sublime.log_commands(True)
			elif t == 'cmd0':
				sublime.log_commands(False)
			elif t == 'ipt1':
				sublime.log_input(True)
			elif t == 'ipt0':
				sublime.log_input(False)
			else:
				em('Unknow abbr!')


	def run(self, edit):
		self.window = self.view.window()
		self.selection = sublime.Selection(self.view.id())

		self.window.show_input_panel("Haiku cmd: ", "", self.on_done, None, None)