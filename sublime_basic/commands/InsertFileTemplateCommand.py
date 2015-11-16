import sublime
import sublime_plugin
import os
from xml.etree import ElementTree
from .SublimeBasic import Basic

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
            folder = folders[0] + '/'
            filename = filename.replace(folder, '')

        namespaces = Basic().get_psr4_namespaces()

        if namespaces:
            for namespace, folder in namespaces.items():
                if folder in filename:
                    namespace = namespace.replace('\\', '/')
                    filename = filename.replace(folder, namespace)

                    # Now extract the namespace and classname
                    namespace = os.path.dirname(filename).replace('/', '\\')
                    classname = os.path.basename(filename).replace('.php', '')

                    xml = ElementTree.parse(template)
                    snippet = xml.getroot().find('content').text
                    sublime.active_window().run_command('insert_snippet', dict(contents=snippet, NAMESPACE=namespace, CLASSNAME=classname))