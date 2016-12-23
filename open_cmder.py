import sublime, sublime_plugin
import os

def md(*t, **kwargs):
	t = kwargs.get('sep', ' ').join([str(el) for el in t])
	sublime.message_dialog(t)

def sm(*t, **kwargs):
	t = kwargs.get('sep', ' ').join([str(el) for el in t])
	sublime.status_message(t)

def em(*t, **kwargs):
	t = kwargs.get('sep', ' ').join([str(el) for el in t])
	sublime.error_message(t)

class OpenCmderCommand(sublime_plugin.WindowCommand):

	def get_setting(self, name, default=None):
		return self.settings.get(name) or default

	def run(self, paths=[]):
		self.view = sublime.active_window().active_view()
		self.selection = sublime.Selection(self.view.id())
		self.settings = self.view.settings()

		cmder_path = self.settings.get("cmder_path", "C:/cmder/cmder.exe")
		def open_cmder(path):
			cmd = '"{}" /SINGLE "{}"'.format(cmder_path, path)
			os.popen(cmd)

		if len(paths) >= 1:
			for item in paths:
				if not os.path.isdir(item):
					item = os.path.dirname(item)
				open_cmder(item)
			return

		project_data = self.window.project_data()

		if project_data:
			path = project_data['folders'][0]['path']
		else:
			path = os.path.dirname(self.view.file_name())

		if not os.path.exists(cmder_path):
			return em("The path '{}' does not exits!".format(cmder_path))

		sm('Opening cmder from "{}"'.format(cmder_path))
		open_cmder(path)
