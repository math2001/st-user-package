import sublime, sublime_plugin
import os.path

class CustomFindInFilesCommand(sublime_plugin.TextCommand):

	def run(self, edit, *args, **kwargs):

		window = self.view.window()

		if self.view.file_name():
			window.run_command("show_panel", {"panel": "find_in_files",
				"where": os.path.dirname(self.view.file_name())})
		elif window.project_data():
			window.run_command("show_panel", {"panel": "find_in_files",
				"where": window.project_data()['folders'][0]['path'] })
		else:
			window.run_command("show_panel", {"panel": "find_in_files"})
