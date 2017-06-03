# -*- coding: utf-8 -*-

"""
Anki Add-on: File Hyperlinks in the Reviewer

Parses the Reviewer for a custom URL scheme and inserts links
that invoke external programs.

Copyright: (c) Glutanimate 2017
License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
"""

#### USER CONFIGURATION START ####

# path to external script or app that handles files

# Windows
external_handler_win = r"C:\Users\AnkiUser\script.exe"

# Unix (Linux/macOS)
external_handler_unix = r"notify-send"

#### USER CONFIGURATION END ####

from subprocess import check_output
import re

from aqt.utils import tooltip
from aqt.reviewer import Reviewer
from anki.hooks import wrap

from anki.utils import isWin

regex_link = r"(qv.+?\..+?\b(#\b.+?\b)?)"
replacement = r"""<a href='' class="flink" onclick='py.link("open:\1");return false;'>\1</a>"""

def openFileHandler(file):
    print file
    try:
        if isWin:
            external_handler = external_handler_win
        else:
            external_handler = external_handler_unix
        out = check_output([external_handler, file])
    except OSError:
        tooltip("External handler produced an error.<br>"
            "Please confirm that it is assigned correctly.")

def linkHandler(self, url, _old):
    if not url.startswith("open"):
        return _old(self, url)
    (cmd, arg) = url.split(":", 1)
    openFileHandler(arg)


def linkInserter(html):
    return re.sub(regex_link, replacement, html)


def onMungeQA(self, buf, _old):
    buf = _old(self, buf)
    return linkInserter(buf)

Reviewer._linkHandler = wrap(Reviewer._linkHandler, linkHandler, "around")
Reviewer._mungeQA = wrap(Reviewer._mungeQA, onMungeQA, "around")