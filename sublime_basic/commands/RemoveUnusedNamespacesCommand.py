import time
import sublime
import sublime_plugin
from ..utils import Utils
from ..classes.Project import Project
from ..classes.PhpParser import PhpParser

#--------------------------------------------------------
# Remove unused namespaces
#--------------------------------------------------------
class RemoveUnusedNamespacesCommand(sublime_plugin.TextCommand):

    """Constructor"""
    def run(self, edit):
        view = self.view
        php = PhpParser()

        dependencies = php.get_dependencies(view)
        imported = php.get_imported_classes(view)

        # Include a possible namespace in the dependencies
        dependencies = list(map(lambda dep: php.include_namespace(view, dep), dependencies))

        # Compare the used classes vs the imported classes
        unused, unimported = php.get_unimported(view, dependencies, imported)

        for region in unused:
            view.erase(edit, view.line(region))