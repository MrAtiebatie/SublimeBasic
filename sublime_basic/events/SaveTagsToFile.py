import os
import re
import glob
import sublime
import sublime_plugin
from ..utils import Utils

class SaveTagsToFile(sublime_plugin.EventListener):
    def on_post_save_async(self, view):
        if view.file_name().endswith('.php'):
            # print('hoi sjors')
            view.file_name()