#!/usr/bin/env python3

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout

from hunter import hunt_keywords
from os.path import dirname, isdir, join

import os
import shutil

class HunterWindow(App):
    def __init__(self):
        super().__init__()

        self.text = ""

    def build(self):
        Window.bind(
            on_dropfile=self._on_file_drop
        )

        layout = BoxLayout(orientation='vertical')
        text = TextInput(text=self.text)

        layout.add_widget(text)

        text.bind(text=self.set_text)

        return layout

    def _on_file_drop(self, window, path):
        if not isdir(path):
            path = dirname(path)

        if type(path) is not str:
            path = path.decode('utf-8')

        output_dir = join(dirname(path), 'Output')
        os.mkdir(output_dir)

        files = hunt_keywords(self.text.split('\n'), path)

        for cpr, paths in files.items():
            cpr_dir = join(output_dir, str(cpr))
            os.mkdir(cpr_dir)

            for path in paths:
                shutil.copy(path, cpr_dir)

    def set_text(self, widget, text):
        self.text = text

if __name__ == '__main__':
    HunterWindow().run()
