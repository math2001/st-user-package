import sublime, sublime_plugin
from re import sub, split, IGNORECASE
import os

def md(*t):
	t = ' '.join([str(txt) for txt in t])
	sublime.message_dialog(t)

class TransformPhpCommand(sublime_plugin.TextCommand):

	def m(self, text):
		sublime.message_dialog(str(text))	

	def run(self, edit):
		for region in self.view.sel():
			syntax = split(r'[\.\/]', self.view.settings().get('syntax'))[-2].lower()
			syntax = self.view.scope_name(region.begin())

			if 'source.php' in self.view.scope_name(region.begin()):
				line = self.view.line(region)

				text = self.view.substr(line)

				text = sub(r'(\w)d ', r'\1math2001_d_ ', text)
				text = sub(r'(\w)i ', r'\1math2001_i_ ', text)
				# dollars : $
				text = sub(r'd ', r'$', text)

				# method : ->
				text = sub(r' m ', r'->', text)

				# index : ["index"]
				text = sub(r' ?i +([\w\-]+)', r"['\1']", text)
				text = sub(r' ?i +([\w\-\$>]+)', r"[\1]", text)

				# define index : "key" => "value"
				text = sub(r'([\'"]) (is|are) ', r'\1 => ', text)

				# superglobal
				text = sub(r'([^a-zA-Z0-9_>\'"\$])dserver([^a-zA-Z0-9_>\'"\$])', r'\1$_SERVER\2', text)
				text = sub(r'([^a-zA-Z0-9_>\'"\$])dget([^a-zA-Z0-9_>\'"\$])', r'\1$_GET\2', text)
				text = sub(r'([^a-zA-Z0-9_>\'"\$])dpost([^a-zA-Z0-9_>\'"\$])', r'\1$_POST\2', text)
				text = sub(r'([^a-zA-Z0-9_>\'"\$])dsession([^a-zA-Z0-9_>\'"\$])', r'\1$_SESSION\2', text)

				elements = [';', '?>', 'if', 'else', '{', "=>", "empty", "isset", "==", 'function', 'class']

				append_semicolon = True
				for element in elements:
					if element in text or ('[' in text and not ']' in text):
						append_semicolon = False

				if append_semicolon:
					text += ';'
					self.view.run_command('move', {"by": "characters", "forward": False})


				text = sub(r'math2001_d_', r'd', text)
				text = sub(r'math2001_i_', r'i', text)
				self.view.replace(edit, line, text)
