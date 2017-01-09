import sublime, sublime_plugin
import os

def md(*t, **kwargs): sublime.message_dialog(kwargs.get('sep', ' ').join([str(el) for el in t]))

def sm(*t, **kwargs): sublime.status_message(kwargs.get('sep', ' ').join([str(el) for el in t]))

def em(*t, **kwargs): sublime.error_message(kwargs.get('sep', ' ').join([str(el) for el in t]))

class EscapeBackslashesCommand(sublime_plugin.TextCommand):

	def run(self, edit, *args, **kwargs):
		for region in self.view.sel():
			self.view.replace(edit, region, self.view.substr(region).replace('\\', '\\\\'))

class EscapeBackslashesListener(sublime_plugin.EventListener):

    def on_text_command(self, view, command, args):
        return
        if command != 'paste':
            return
        if view.settings().get('escape_path_on_paste') is True:
            if '\n' in clipboard:
                return
            clipboard = sublime.get_clipboard()
            if 'string' in view.scope_name(view.sel()[0].begin()):
                sublime.set_clipboard(clipboard.replace('\\', '\\\\') \
                                               .strip('"\''))
            else:
                sublime.set_clipboard(clipboard.replace('\\', '\\\\'))
            view.run_command('paste')
            sublime.set_clipboard(clipboard)
            return 'none'
