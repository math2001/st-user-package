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

class DeletePycCommand(sublime_plugin.TextCommand):

	def get_setting(self, name, default=None):
		return self.settings.get(name) or default

	def remove_pyc(self, path):
		for file in os.listdir(path):
			if '.' not in file:
				# it's a folder
				self.remove_pyc(os.path.join(path, file))
			if file.split('.')[-1] == 'pyc':
				os.remove(os.path.join(path, file))

	def run(self, edit, *args, **kwargs):
		self.window = self.view.window()
		self.selection = sublime.Selection(self.view.id())
		self.settings = self.view.settings()

		def move_file(path, new_path):
			if os.path.exists(new_path):
				return False
			with open(path, 'r') as fp:
				content = fp.read()
			with open(new_path, 'w') as fp:
				fp.write(content)
			return True


		project = self.window.project_data()['folders']
		for folder in project:
			self.remove_pyc(folder['path'])


