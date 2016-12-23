import sublime, sublime_plugin

class CenterScreenCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		self.view.show_at_center(self.view.sel()[0].begin())

