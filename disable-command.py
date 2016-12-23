import sublime_plugin

class RunScriptCommand(sublime_plugin.TextCommand):
	def run(self, *args, **kwargs):
		pass

	def is_enabled(self):
		return False
	def is_visible(self):
		return False
