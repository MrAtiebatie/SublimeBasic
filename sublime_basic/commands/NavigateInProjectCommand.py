import os
import sublime
import sublime_plugin
from ..utils import Utils

#--------------------------------------------------------
# Navigate in project plugin
#--------------------------------------------------------
class NavigateInProjectCommand(sublime_plugin.TextCommand):
    path = ""
    folders = []
    files = []

    def run(self, edit):
        self.path = Utils.project_path()

        self.quick_panel_folder(self.path)

    def quick_panel_folder(self, folder):
        """ Show folder contents """
        folders = [["./", "Previous"]]
        files = []

        exclude = Utils.settings("folder_exclude_patterns", [], "Preferences.sublime-settings")

        self.path = folder

        # Get all dirs
        for name in os.listdir(folder):
            if os.path.isdir(os.path.join(folder, name)) and not any(name in s for s in exclude):
                folders.append([name, "Folder"])

        # Get all regular files
        for name in os.listdir(folder):
            if os.path.isfile(os.path.join(folder, name)):
                files.append([name, "File"])

        # Show selection panel
        self.contents = folders + files
        self.view.window().show_quick_panel(self.contents, self.navigate, sublime.KEEP_OPEN_ON_FOCUS_LOST, 1)

    # Show next folder
    def navigate(self, item):
        if item == -1:
            return

        if self.contents[item]:
            item = self.contents[item]
            item = self.path + "/" + item[0]

            if os.path.isfile(item):
                sublime.active_window().open_file(item)
            else:
                self.quick_panel_folder(item)

