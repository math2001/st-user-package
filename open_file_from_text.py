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

# cat.bat:10

class OpenFileFromTextCommand(sublime_plugin.TextCommand):

	def get_setting(self, name, default=None):
		return self.settings.get(name) or default

	def _look_for(self, file_name, on_found, *args, **kwargs):
		project = self.window.project_data()['folders']
		for path in [p['path'] for p in project]:
			rtn = self._look_for_deep(path, file_name, on_found, *args, **kwargs)
		return rtn


	def _look_for_deep(self, path, file_name, on_found, *args, **kwargs):
		for file in os.listdir(path):
			if '.' not in file:
				self._look_for_deep(os.path.join(path, file), file_name, on_found, *args, **kwargs)
			elif file == file_name:
				return on_found(os.path.join(path, file), *args, **kwargs)

	def on_found(self, path, line):
		self.window.open_file(path + ':' + line, sublime.ENCODED_POSITION)

	def run(self, edit, *args, **kwargs):
		self.window = self.view.window()
		self.selection = sublime.Selection(self.view.id())
		self.settings = self.view.settings()



		char = ''
		for region in self.view.sel():
			begin = region.begin()
			while char not in (' ', '?', '!', '\n'):
				begin -= 1
				char = self.view.substr(begin)
				if begin <= 0:
					char = ' '
			begin += 1

			end = region.end()
			char = ''
			while char not in (' ', '?', '!', '\n'):
				end += 1
				char = self.view.substr(end)
				if end >= self.view.size():
					char = ' '
			text = self.view.substr(sublime.Region(begin, end)).split(':')
			view = self._look_for(text[0], self.on_found, text[1])
			self.window.focus_view(view)
