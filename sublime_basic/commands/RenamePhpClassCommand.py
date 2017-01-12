import sublime
import sublime_plugin
import os
import fileinput
import ntpath
import string
from ..utils import Utils

#--------------------------------------------------------
# Rename PHP class
#--------------------------------------------------------
class RenamePhpClassCommand(sublime_plugin.TextCommand):

    def run(self, edit, paths = []):
        self.file = paths[0]

        if not self.file.endswith(".php"):
            return

        filename = self.file.split("/").pop().replace(".php", "")

        self.view.window().show_input_panel("Rename", filename, self.rename, None, None)

    def rename(self, filename):
        if filename is None:
            return

        if not filename.endswith(".php"):
            filename = filename + ".php"

        old_file = ntpath.basename(self.file)
        new_file = self.file.replace(old_file, filename)

        # Rename file
        os.rename(self.file, new_file)

        # Close file
        self.view.set_scratch(True)
        self.view.close()

        # Change class name
        new_class_file = ntpath.basename(new_file)
        class_name     = os.path.splitext(old_file)[0]
        new_class_name = os.path.splitext(new_class_file)[0]

        for line in fileinput.FileInput(new_file, inplace=True):
            print(line.replace(class_name, new_class_name), end='')

        self.view.window().open_file(new_class_file)
