import sublime, sublime_plugin
import os
import webbrowser

def md(*t, **kwargs): sublime.message_dialog(kwargs.get('sep', ' ').join([str(el) for el in t]))

def sm(*t, **kwargs): sublime.status_message(kwargs.get('sep', ' ').join([str(el) for el in t]))

def em(*t, **kwargs): sublime.error_message(kwargs.get('sep', ' ').join([str(el) for el in t]))

PATH_TO_PYGAME_DOC = 'file://C:/Users/math/python/Lib/site-packages/pygame/docs/ref'

class OpenPygameDocCommand(sublime_plugin.TextCommand):

	def run(self, edit, *args, **kwargs):
		self.window = self.view.window()
		self.selection = sublime.Selection(self.view.id())
		self.settings = self.view.settings()

		for region in self.view.sel():

			# pygame.draw.circle

			text = self.view.substr(region)
			text = 'pygame.draw.circle'
			if text.startswith('pygame.'):
				text = text[len('pygame.'):]

			module, method = text.split('.')

			path = PATH_TO_PYGAME_DOC + '/' + module + '.html#' + module + '.' + method

			webbrowser.open_new_tab(path)


