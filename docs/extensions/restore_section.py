# This file is part of the MicroPython project, http://micropython.org/
#
# The MIT License (MIT)
#
# Copyright (c) 2023 Jim Mussared
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Sphinx/rST provides no way to "end" a section, which means that when we
# use the `autoclass` directive (when not using `:members:` on `automodule`),
# the class documentation will be injected at the current section/heading
# level.

# This means that as far as the TOC is concerned, using `autoclass` will
# produce a different result if there is a heading before the `autoclass`, for
# example some sort of "Overview" section or similar, compared to if the
# `autoclass` comes directly after the `automodule`. In the former case, the
# class will be "inside" the overview section, and therefore not appear in the
# TOC, whereas in the second case, it will be at the top-level and get a TOC
# entry.

# This Sphinx extension provides a directive that generates no content resets
# the current state to the top-level heading (i.e. as if the state was
# currently before the first "----" style heading, typically module
# top-level).

# See docutils/parsers/rst/states.py, where RSTState.section (used in lots
# of places to start a section) first uses `check_subsection` to get into
# the correct state for the given section style, then `new_subsection` to
# actually enter the new section state. We just do the first part.

from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.application import Sphinx
class RestoreSection(Directive):
    def run(self):
        self.state.check_subsection(source="", style="-", lineno=0)
        return []

def setup(app:Sphinx):
    app.add_directive("restore_section", RestoreSection)

    return {
        'version': '1.0',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
