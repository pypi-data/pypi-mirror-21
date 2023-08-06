#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Custom tab widget."""


from html import entities

from PyQt5.QtWidgets import QApplication, QPushButton

from unicodemoticon.core.scrollgroup import ScrollGroup


class TabHtml(ScrollGroup):

    """Custom tab widget."""

    def __init__(self, parent=None, *args, **kwargs):
        """Init class custom tab widget."""
        super(TabHtml, self).__init__(self, *args, **kwargs)
        self.parent = parent
        self.setParent(parent)

        added_html_entities, row, index = [], 0, 0
        for html_char in tuple(sorted(entities.html5.items())):
            added_html_entities.append(
                html_char[0].lower().replace(";", ""))
            if not html_char[0].lower() in added_html_entities:
                button = QPushButton(html_char[1], self)
                button.released.connect(self.parent.hide)
                button.pressed.connect(lambda ch=html_char:
                                       self.parent.make_preview(str(ch)))
                button.clicked.connect(
                    lambda _, ch=html_char[0]:
                    QApplication.clipboard().setText(
                        "&{html_entity}".format(html_entity=ch)))
                button.setToolTip("<center><h1>{0}<br>{1}".format(
                    html_char[1],
                    self.parent.get_description(html_char[1])))
                button.setFlat(True)
                font = button.font()
                font.setPixelSize(50)
                button.setFont(font)
                index = index + 1  # cant use enumerate()
                row = row + 1 if not index % 8 else row
                self.layout().addWidget(button, row, index % 8)
