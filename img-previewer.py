import sublime, sublime_plugin
import os

def md(*t, **kwargs): sublime.message_dialog(kwargs.get('sep', ' ').join([str(el) for el in t]))

def sm(*t, **kwargs): sublime.status_message(kwargs.get('sep', ' ').join([str(el) for el in t]))

def em(*t, **kwargs): sublime.error_message(kwargs.get('sep', ' ').join([str(el) for el in t]))

def any_in(els_to_test, el_to_test):
	for el in els_to_test:
		if el in el_to_test:
			return True
	return False

def all_in(els_to_test, el_to_test):
	for el in els_to_test:
		if el not in el_to_test:
			return False
	return True

def unquote(str):
	if str[0] in ['"', "'"]:
		str = str[1:]
	if str[-1] in ['"', "'"]:
		str = str[:-1]
	return str

class ImagePreviewerCommand(sublime_plugin.TextCommand):

	def run(self, edit, *args, **kwargs):
		# return self.view.show_popup('why not?', location=0)
		self.window = self.view.window()
		self.selection = sublime.Selection(self.view.id())
		self.settings = self.view.settings()

		sel = self.view.sel()[0]

		if not all_in(['text.html', 'string'], self.view.scope_name(sel.begin())):
			return False

		for region in self.view.find_by_selector('string.quoted.double.html'):
			if region.contains(sel):

				path = unquote(self.view.substr(region))
				if not (
					path.startswith('http://') or
					path.startswith('https://') or
					path.startswith('file://')
				):
					path = 'file://' + os.path.join(os.path.dirname(self.view.file_name()), path).replace(os.path.sep, '/')
				html = """
<style>
	body { margin: 0; }
</style>
<body>
	<img src=[path]>
</body>
				""".replace('[path]', path)
				return self.view.show_popup(html)
