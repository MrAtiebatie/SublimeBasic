import sublime
import sublime_plugin

#--------------------------------------------------------
# Select All Classes Plugin
#--------------------------------------------------------
class SelectAllClassesCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view

        view.sel().clear()

        view.sel().add_all(view.find_by_selector('support.class.php'))
        view.sel().add_all(view.find_by_selector('entity.other.inherited-class.php'))

        for usage in view.find_by_selector('meta.use.php meta.path.php support.class.php'):
            view.sel().subtract(usage)