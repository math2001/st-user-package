import sublime, sublime_plugin
import os

def md(*args): sublime.message_dialog(' '.join([str(arg) for arg in args]))

class SnippetListerCommand(sublime_plugin.TextCommand):

	def __list_all_snippets(self, path=None, all_snippets=[]):
		if path is None: path = self.SNIPPETS_PATH
		for item in os.listdir(path):
			if os.path.isdir(os.path.join(path, item)):
				self.__list_all_snippets(os.path.join(path, item), all_snippets)
			else:
				all_snippets.append(
					os.path.join(path, item).replace(self.SNIPPETS_PATH, '').replace(
						os.path.sep, '/')[1:])
		return all_snippets

	def on_done(self, index):
		if index == -1:
			return self.window.run_command('close')
		path = os.path.join(self.SNIPPETS_PATH, self.all_snippets[index])
		self.window.open_file(path)

	def on_highlighted(self, index):
		path = os.path.join(self.SNIPPETS_PATH, self.all_snippets[index])
		self.window.open_file(path, sublime.TRANSIENT)

	def run(self, edit, *ars, **kwargs):
		self.window = self.view.window()
		self.SNIPPETS_PATH = os.path.join(sublime.packages_path(), 'user', 'snippets')

		self.all_snippets = self.__list_all_snippets()

		self.window.show_quick_panel(self.all_snippets, self.on_done, 0, 50, self.on_highlighted)
