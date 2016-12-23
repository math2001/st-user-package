# CSW: ignore
# -*- encoding: utf-8 -*-

import sublime
import sublime_plugin

class LoggerCommand(sublime_plugin.ApplicationCommand):

    log = None
    last_index = 0

    def is_enabled(self):
        return False

    def on_done(self, index):
        if index == -1:
            return
        if index == 0 and LoggerCommand.log != None:
            LoggerCommand.log = None
        LoggerCommand.log = self.formats[index]
        LoggerCommand.last_index = index

    def run(self, format_=None):
        self.formats = ['Sublime', 'Python']
        if LoggerCommand.log != None:
            self.formats.insert(0, 'Disable')
        if format_ is None:
            sublime.active_window().show_quick_panel(self.formats, self.on_done, 0, LoggerCommand.last_index)
        elif format_ in self.formats:
            LoggerCommand.log = format_
        elif format_ is False:
            LoggerCommand.log = None
        else:
            raise ValueError('The format is invalid. It must be on of those: {0}'.format(self.formats + [False]))


class LoggerListenerCommand(sublime_plugin.EventListener):

    not_logged_commands = ['drag_select', 'left_delete', 'right_delete']

    def on_window_command(self, view, command, args):
        if LoggerCommand.log == 'Sublime':
            print('"command": "{0}"'.format(command) + ', "args": {0}'.format(str(args).replace("'", '"')) if args is not None else '')
        elif LoggerCommand.log == 'Python':
            print('command: "{0}"'.format(command) + ', {0}'.format(args).replace("'", '"') if args is not None else '')

    def on_text_command(self, view, command, args):
        if command not in LoggerListenerCommand.not_logged_commands:
            self.on_window_command(view, command, args)
