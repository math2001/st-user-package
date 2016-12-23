import sublime
import sublime_plugin
import os
import json

class PromptOpenRecentProjectCommand(sublime_plugin.WindowCommand):

    def run(self):
        self.recent_workspaces = self.get_recent_workspaces()
        if not self.recent_workspaces:
            return sublime.error_message('No project to load!')

        for i, recent_workspace in enumerate(self.recent_workspaces):
            self.recent_workspaces[i] = recent_workspace.replace('C/', 'C:/').strip('/')


        # only display workspaces that really exist
        self.recent_workspaces_that_really_exist = []
        for recent_workspace in self.recent_workspaces:
            if os.path.isfile(recent_workspace):
                self.recent_workspaces_that_really_exist.append(recent_workspace)

        sublime.message_dialog(str(self.recent_workspaces_that_really_exist))
        self.window.show_quick_panel(self.recent_workspaces_that_really_exist, self.on_done)

    def on_done(self, index):
        if index == -1:
            return

        picked = self.recent_workspaces_that_really_exist[index];
        index = self.recent_workspaces.index(picked)

        self.window.run_command('open_recent_project_or_workspace', {'index': index})

    def get_recent_workspaces(self):
        """
        Returns an list > 0; otherwise None
        """

        session = self.load_session()
        if not session:
            return None

        workspaces = session.get('workspaces')
        if not workspaces:
            return None

        recent_workspaces = workspaces.get('recent_workspaces')
        if not recent_workspaces:
            return None

        # substitute user home dir with ~
        # user_home_dir = os.getenv('HOME')
        # recent_workspaces_list = []
        # for recent_workspace in recent_workspaces:
        #     if recent_workspace.startswith(user_home_dir):
        #         recent_workspaces_list.append(recent_workspace.replace(user_home_dir, '~'))
        #     else:
        #         recent_workspaces_list.append(recent_workspace)

        # if recent_workspaces_list and len(recent_workspaces_list) > 0:
        #     return recent_workspaces_list
        return recent_workspaces

        return None

    def load_session(self):
        """
        Returns dict or None if no session exists
        """

        local_session_path = os.path.join(os.path.dirname(sublime.packages_path()), 'Local')
        local_auto_save_session_file = os.path.join(local_session_path, 'Auto Save Session.sublime_session')
        local_session_file = os.path.join(local_session_path, 'Session.sublime_session')

        if os.path.isfile(local_auto_save_session_file):
            session_file_to_use = local_auto_save_session_file
        elif os.path.isfile(local_session_file):
            session_file_to_use = local_session_file
        else:
            return None

        with open(session_file_to_use) as f:
            local_session_content = f.read()

        session = json.loads(local_session_content, strict=False)

        return session