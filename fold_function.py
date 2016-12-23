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

class FoldFunctionCommand(sublime_plugin.TextCommand):

	def run(self, edit, *args, **kwargs):

		self.window = self.view.window()
		self.selection = sublime.Selection(self.view.id())
		self.settings = self.view.settings()

		self.view.unfold(sublime.Region(0, self.view.size()))

		functions = self.view.find_by_selector('entity.name.function')
		self.selection.clear()
		self.selection.add_all(functions)
		self.view.run_command('move', { 'by': "lines", "forward": True })

		sel = self.view.sel()[0]
		if self.view.substr(self.view.line(sel)) == '{':
			self.view.run_command('move', { 'by': "lines", "forward": True })

		"""
			Support for:
			function something() {
				// code
			}
			function ()
			{
				// code
			}
			This last example is the reason of the last condition
		"""

		self.view.run_command('fold')
		self.selection.clear()

		return
