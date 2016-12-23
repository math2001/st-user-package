import sublime, sublime_plugin
import os

def md(*t, **kwargs): sublime.message_dialog(kwargs.get('sep', ' ').join([str(el) for el in t]))

def sm(*t, **kwargs): sublime.status_message(kwargs.get('sep', ' ').join([str(el) for el in t]))

def em(*t, **kwargs): sublime.error_message(kwargs.get('sep', ' ').join([str(el) for el in t]))


class OpenJsFromCoffeeCommand(sublime_plugin.TextCommand):


	"""
		Open the corresponding js file from the current view (a coffeescript one)

		structures:

		<js> 					 # whatever
			<coffee> 			 # whatever
				- script.coffee
				- ...
			- script.js
			- ...

	"""



	def run(self, edit, *args, **kwargs):
		self.settings = self.view.settings()
		self.window = self.view.window()
		self.selection = sublime.Selection(self.view.id())
		# self.settings = self.view.settings()

		if not self.is_enabled():
			return em('Cannot run: not a .coffee file!')

		fullpath = self.view.file_name()
		path = os.path.dirname(os.path.dirname(fullpath))
		filename, ext = os.path.splitext(os.path.basename(fullpath))
		path = os.path.join(path, filename) + '.js'
		if not os.path.exists(path):
			return em("The path '{}' does not exists!".format(path))

		self.window.run_command("new_pane", {"move": False})
		view = self.window.open_file(path)
		self.window.set_view_index(view, 1, 0)


	def is_enabled(self):
		return 'coffee' in self.view.settings().get('syntax').lower() and \
		self.view.file_name() is not None
