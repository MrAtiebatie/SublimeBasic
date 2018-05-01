import sublime
import sublime_plugin
from ..utils import Utils

class CheckNamespacesEvent(sublime_plugin.EventListener):
    def on_post_save(self, view):
        if view.file_name().endswith(".php"):
            view.run_command("remove_unused_namespaces")
            view.run_command("check_namespaces")