import sublime
import sublime_plugin
import os
import difflib
from xml.etree import ElementTree
from ..utils import Utils

#--------------------------------------------------------
# Insert file template
#--------------------------------------------------------
class InsertFileTemplateCommand(sublime_plugin.TextCommand):

    def run(self, edit, template):
        window = sublime.active_window()
        view = self.view

        # Path variables
        folders = window.folders()
        filename = view.file_name()
        if len(folders) > 0:
            folder = folders[0] + "/"
            filename = filename.replace(folder, "")

        namespaces = Utils().get_psr4_namespaces()

        if namespaces:
            current = os.path.dirname(filename)

            folders = namespaces.values()
            psrfolder = difflib.get_close_matches(current, folders)

            namespace = ""

            if any(folder for folder in folders if current.startswith(folder)):
                directory = [folder for folder in folders if current.startswith(folder)]

                for (key, value) in namespaces.items():
                    if value == directory[0]:
                        namespace = current.replace(value, key).replace("/", "\\")

            classname = os.path.basename(filename).replace(".php", "")
            xml       = ElementTree.parse(template)
            snippet   = xml.getroot().find("content").text

            sublime.active_window().run_command("insert_snippet", dict(contents=snippet, NAMESPACE=namespace, CLASSNAME=classname))
            sublime.active_window().run_command("save")
