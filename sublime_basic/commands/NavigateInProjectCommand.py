import os
import sublime
import sublime_plugin
from ..utils import Utils

#--------------------------------------------------------
# Navigate in project plugin
#--------------------------------------------------------
class NavigateInProjectCommand(sublime_plugin.TextCommand):
    folders = []
    files = []

    def run(self, edit):
        project = Utils.project_path(self)

        self.quick_panel_folder(project)

    def quick_panel_folder(self, folder):
        folders = []
        files = []

        # Get all dirs
        for name in os.listdir(folder):
            if os.path.isdir(os.path.join(folder, name)):
                folders.append([name])

        # Get all regular files
        for name in os.listdir(folder):
            if os.path.isfile(os.path.join(folder, name)):
                files.append(name)

        self.folders = folders
        self.files = files

        self.view.window().show_quick_panel(self.folders + self.files, self.navigate)

    # Show next folder
    def navigate(self, item):
        if item == -1:
            return

        if self.folders[item]:
            item = self.content[item]
            folder = self.project + "/" + item

