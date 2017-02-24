import sublime, sublime_plugin
import os

def md(*t, **kwargs): sublime.message_dialog(kwargs.get('sep', ' ').join([str(el) for el in t]))

def sm(*t, **kwargs): sublime.status_message(kwargs.get('sep', ' ').join([str(el) for el in t]))

def em(*t, **kwargs): sublime.error_message(kwargs.get('sep', ' ').join([str(el) for el in t]))

class EscapeBackslashesCommand(sublime_plugin.TextCommand):

    def run(self, edit, *args, **kwargs):
        for region in self.view.sel():
            if region.empty():
                region = self.view.extract_scope(region.begin())
            self.view.replace(edit, region, self.view.substr(region).replace('\\', '\\\\'))
