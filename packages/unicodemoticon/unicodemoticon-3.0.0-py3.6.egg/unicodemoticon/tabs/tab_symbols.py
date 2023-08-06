#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Custom tab widget."""


from html import entities

from PyQt5.QtWidgets import QApplication, QPushButton

from unicodemoticon.core.scrollgroup import ScrollGroup


class TabSymbols(ScrollGroup):

    """Custom tab widget."""

    def __init__(self, parent=None, *args, **kwargs):
        """Init class custom tab widget."""
        super(TabSymbols, self).__init__(self, *args, **kwargs)
        self.parent = parent
        self.setParent(parent)

        added_symbols, row, index = [], 0, 0
        for html_char in tuple(sorted(entities.html5.items())):
            html_char = str(html_char[1]).lower().strip()
            if html_char not in added_symbols and len(html_char):
                button = QPushButton(html_char, self)
                button.released.connect(self.parent.hide)
                button.pressed.connect(lambda ch=html_char:
                                       self.parent.make_preview(ch))
                button.clicked.connect(
                    lambda _, ch=html_char:
                    QApplication.clipboard().setText(str(ch)))
                button.setToolTip("<center><h1>{0}<br>{1}".format(
                    html_char,
                    self.parent.get_description(html_char)))
                button.setFlat(True)
                font = button.font()
                font.setPixelSize(50)
                button.setFont(font)
                index = index + 1  # cant use enumerate()
                row = row + 1 if not index % 8 else row
                self.layout().addWidget(button, row, index % 8)
                added_symbols.append(html_char)
