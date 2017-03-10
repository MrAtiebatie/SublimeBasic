import sublime
import sublime_plugin

class PromptCopyLineCommand(sublime_plugin.WindowCommand):

    def run(self):
        self.window.show_input_panel("Copy Line:", "", self.on_done, None, None)
        pass

    def on_done(self, text):
        try:
            line = int(text)
            if self.window.active_view():
                self.window.active_view().run_command("copy_line", {"line": line} )
        except ValueError:
            pass

class CopyLineCommand(sublime_plugin.TextCommand):

    def run(self, edit, line):
        # Convert from 1 based to a 0 based line number
        line = int(line) - 1

        # Negative line numbers count from the end of the buffer
        if line < 0:
            lines, _ = self.view.rowcol(self.view.size())
            line = lines + line + 1

        pt = self.view.text_point(line, 0)
        line = self.view.substr(self.view.line(pt)).strip()

        for sel in self.view.sel():
            self.view.insert(edit, sel.begin(), line)
