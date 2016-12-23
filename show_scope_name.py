import sublime
import sublime_plugin


def copy(view, text):
	sublime.set_clipboard(text)
	view.hide_popup()
	sublime.status_message('Scope name copied to clipboard')


class ShowScopeNameCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		whole_scope = self.view.scope_name(self.view.sel()[-1].b)
		scopes = whole_scope.strip().split(' ')

		paragraphs = ''
		for scope in scopes:
			paragraphs += '<p><a href="{0}">Copy</a> {0}</p>'.format(scope)
		html = """
			<body id="show-scope">
				<style>
					body {
						padding: 5px;
						margin: 0;
					}
					p {
						margin: 10px;
					}
				</style>
				%s
				<p><a href="%s">Everything</a></p>
			</body>
		""" % (paragraphs, whole_scope)



		self.view.show_popup(html, max_width=512, on_navigate=lambda x: copy(self.view, x))