markdust
========

[![Documentation Status](https://readthedocs.org/projects/markdust/badge/)](http://markdust.readthedocs.io/en/latest/?badge)

[![Coverage Status](https://cdn.rawgit.com/thespacedoctor/markdust/master/coverage.svg)](https://cdn.rawgit.com/thespacedoctor/markdust/master/htmlcov/index.html)

*A python package and command-line tools for A bunch of scripts and
command-line tools to help with writting notes, blog-posts and slides*.

Here's a summary of what's included in the python package:

Command-Line Usage
==================

    Documentation for markdust can be found here: http://markdust.readthedocs.org/en/stable

    Usage:
        markdust init

    Options:
        init                  setup the markdust settings file for the first time
        -h, --help            show this help message
        -v, --version         show version
        -s, --settings        the settings file

Documentation
=============

Documentation for markdust is hosted by [Read the
Docs](http://markdust.readthedocs.org/en/stable/) (last [stable
version](http://markdust.readthedocs.org/en/stable/) and [latest
version](http://markdust.readthedocs.org/en/latest/)).

Installation
============

The easiest way to install markdust is to use `pip`:

    pip install markdust

Or you can clone the [github
repo](https://github.com/thespacedoctor/markdust) and install from a
local version of the code:

    git clone git@github.com:thespacedoctor/markdust.git
    cd markdust
    python setup.py install

To upgrade to the latest version of markdust use the command:

    pip install markdust --upgrade

Development
-----------

If you want to tinker with the code, then install in development mode.
This means you can modify the code from your cloned repo:

    git clone git@github.com:thespacedoctor/markdust.git
    cd markdust
    python setup.py develop

[Pull requests](https://github.com/thespacedoctor/markdust/pulls) are
welcomed!

### Sublime Snippets

If you use [Sublime Text](https://www.sublimetext.com/) as your code
editor, and you're planning to develop your own python code with
markdust, you might find [my Sublime
Snippets](https://github.com/thespacedoctor/markdust-Sublime-Snippets)
useful.

Issues
------

Please report any issues
[here](https://github.com/thespacedoctor/markdust/issues).

License
=======

Copyright (c) 2016 David Young

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
