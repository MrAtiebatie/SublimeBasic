import re
import sublime
import sublime_plugin
from ..utils import Utils

#--------------------------------------------------------
# Tokenize File Plugin
#--------------------------------------------------------
class TokenizeFileCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        code = Utils.get_full_view(view)

    def tokenize(str):
        tokens = {}

        # str.replace()
