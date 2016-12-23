import sublime
import sublime_plugin

class ApiReplace(sublime_plugin.TextCommand):

	def run(self, edit, region, text):
		if type(region) in (list, tuple):
			region = sublime.Region(region[0], region[1])
		self.view.replace(edit, region, text)