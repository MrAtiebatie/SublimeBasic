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
        if (len(folders) > 0):
            folder = folders[0] + "/"
            filename = filename.replace(folder, "")

        namespaces = Utils().get_psr4_namespaces()

        if namespaces:
            # for namespace, folder in namespaces.items():
            current = os.path.dirname(filename)

            folders = namespaces.values()
            psrfolder = difflib.get_close_matches(current, folders)

            if len(psrfolder) > 0:
                namespace = [k for k, v in namespaces.items() if v == psrfolder[0]]

                # Now extract the namespace and classname
                if namespace != None:
                    namespace = namespace[0] + current.replace(psrfolder[0], "").replace("/", "")
            else:
                namespace = ""

            classname = os.path.basename(filename).replace(".php", "")
            xml       = ElementTree.parse(template)
            snippet   = xml.getroot().find("content").text

            sublime.active_window().run_command("insert_snippet", dict(contents=snippet, NAMESPACE=namespace, CLASSNAME=classname))
            sublime.active_window().run_command("save")
