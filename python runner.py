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

class PythonRunnerCommand(sublime_plugin.TextCommand):

	def get_setting(self, name, default=None):
		return self.setting.get(name) or default

	def on_done(self, index):
		if index == 1:
			self.window.run_command('build')

	def can_be_run(self, view):
		name = os.path.basename(view.file_name())
		return name == '_main.py' \
			   or ('_.py' in name and name != '__init__.py') \
			   or (os.path.splitext(name)[0] \
			   		== os.path.basename(os.path.dirname(view.file_name())))


	def run(self, edit, *args, **kwargs):
		self.window = self.view.window()
		self.selection = sublime.Selection(self.view.id())
		self.settings = self.view.settings()

		group_index, view_index = self.window.get_view_index(self.view)

		error = True

		def build(view):

			main_group_index, main_view_index = self.window.get_view_index(view)
			view_to_focus = None
			if main_group_index != group_index:
				view_to_focus = self.window.active_view_in_group(main_group_index)
			self.window.focus_view(view)
			self.window.run_command('build')
			if view_to_focus is not None:
				self.window.focus_view(view_to_focus)
			self.window.focus_view(self.view)



		if self.can_be_run(self.view):
			build(self.view)
			return

		for view in self.window.views():
			if self.can_be_run(view):
				build(view)
				error = False
				return

		if error is True:
			self.window.show_quick_panel(
				[
					[
						'Error: no "_main.py" is open.',
						'The plugin won\'t do anything.'
					],
					[
						'Forget it buddy, run this file',
						self.view.file_name()
					],
				],
				self.on_done,
				sublime.KEEP_OPEN_ON_FOCUS_LOST,
				1)
