# -*- encoding: utf-8 -*-

import sublime
import sublime_plugin

class PythonStringHelperCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        BEGIN = 'punctuation.definition.string.begin.python'
        END = 'punctuation.definition.string.end.python'
        regex = r'''\w(['"])\n\s*(['"])'''
        view = self.view

        regions = view.find_all(regex)
        for i, region in enumerate(regions):
            region = sublime.Region(region.begin() + i, region.end() + i)
            if not END in view.scope_name(region.begin() + 1) \
                or not BEGIN in view.scope_name(region.end() - 1):
                continue

            view.insert(edit, region.begin() + 1, ' ')

    def is_enabled(self):
        return 'source.python' in self.view.scope_name(0)


class PythonStringHelperListener(sublime_plugin.EventListener):

    def on_pre_save(self, view):
        view.run_command('python_string_helper')
