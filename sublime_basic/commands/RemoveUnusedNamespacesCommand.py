import time
import sublime
import sublime_plugin
from ..utils import Utils
from ..classes.Project import Project
from ..classes.PhpParser import PhpParser
from ..classes.PhpBuilder import PhpBuilder

#--------------------------------------------------------
# Remove unused namespaces
#--------------------------------------------------------
class RemoveUnusedNamespacesCommand(sublime_plugin.TextCommand):

    """Constructor"""
    def run(self, edit):
        view = self.view
        builder = PhpBuilder()

        builder.clear_use_statements(view, edit)