import sublime
import sublime_plugin

class GroupFileIntoOneCommand(sublime_plugin.EventListener):

    def compile(self, window, settings):
        file_grouper_path = settings.get('file_grouper_path', None)
        if file_grouper_path is None:
            return sublime.error_message("Cannot find 'file_grouper_path' setting: abort building")
        window.run_command('exec', {cmd: file_grouper_path})

    def on_post_save(self, view):
        # check if it is one of the file that you need to compile (using the extension for example)
        return
        self.compile(view.window(), view.settings())
