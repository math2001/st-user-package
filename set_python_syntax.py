# -*- encoding: utf-8 -*-

import sublime_plugin

class SetSyntaxPythonCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        self.view.assign_syntax('Packages/Python/Python.sublime-syntax')
        self.view.settings().set('gutter', False)
