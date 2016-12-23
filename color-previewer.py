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


def any_in(els_to_test, el_to_test):
	for el in els_to_test:
		if el in el_to_test:
			return True
	return False


class ColorPreviewerCommand(sublime_plugin.TextCommand):

	def get_setting(self, name, default=None):
		return self.settings.get(name) or default


	def run(self, edit, *args, **kwargs):
		# return self.view.run_command('api_replace', { 'region': [0, 0], 'text': 'yep' })

		self.window = self.view.window()
		self.selection = sublime.Selection(self.view.id())
		self.settings = self.view.settings()

		to_upper_case = self.settings.get('color_to_upper_case', False)
		# can create bug: if you click on a color, and then click again, it will disappear.

		html = """
			<style>
				div {
					background-color: {bg};
					color: {bg};
					padding: {size}px;
					display: block;
					width: 100%;
					border-radius: 50px;
				}
				body, html {
					margin: 0;
				}
			</style>
			<body id="color">
				<div href="somepage.html"></div>
			</body>
		"""



		point = self.view.sel()[0].begin()
		if 'color' in self.view.scope_name(point):

			region = self.view.word(point)
			color = self.view.substr(region)


			row, col = self.view.rowcol(point)
			point = self.view.text_point(row - 1, 0)
			lenght = len(self.view.line(point))
			def hidden():
				if to_upper_case:
					self.view.run_command('api_replace', { 'region': [region.a, region.b], 'text': color.upper() })
			self.view.show_popup(html.replace('{bg}', color).replace('{size}', '10'),
				location=point,
				on_hide=hidden
			)


# class ColorAutoPreviewerCommand(sublime_plugin.EventListener):

# 	def __init__(self, *args, **kwargs):
# 		sublime_plugin.EventListener.__init__(self, *args, **kwargs)
# 		self.syntax_to_check = ['css', 'stylus', 'postcss', 'sass', 'scss']

# 	def on_post_text_command(self, view, cmd, args):
# 		if any_in(self.syntax_to_check, view.settings().get('syntax').lower()):
# 			view.run_command('color_previewer')
# 		else:
# 			view.hide_popup()

# 	def on_modified(self, view):
# 		if any_in(self.syntax_to_check, view.settings().get('syntax').lower()):
# 			view.hide_popup()
