import sublime
import sublime_plugin


class CloseOtherTabsCommand(sublime_plugin.TextCommand):
    """
    Tells the window to close all other views that share the same group
    in the layout as the current file.
    """
    def run(self, edit):
        group, index = self.view.window().get_view_index(self.view)
        self.view.window().run_command("close_others_by_index", {
            "group": group,
            "index": index
        })