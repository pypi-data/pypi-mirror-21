markdust
========

[![Documentation Status](https://readthedocs.org/projects/markdust/badge/)](http://markdust.readthedocs.io/en/latest/?badge)

[![Coverage Status](https://cdn.rawgit.com/thespacedoctor/markdust/master/coverage.svg)](https://cdn.rawgit.com/thespacedoctor/markdust/master/htmlcov/index.html)

*A python package and command-line tools for A bunch of scripts and command-line tools to help with writting notes, blog-posts and slides*.

Here’s a summary of what’s included in the python package:

Command-Line Usage
==================

``` sourceCode
Documentation for markdust can be found here: http://markdust.readthedocs.org/en/stable

Usage:
    markdust init

Options:
    init                  setup the markdust settings file for the first time
    -h, --help            show this help message
    -v, --version         show version
    -s, --settings        the settings file
```

Installation
============

The easiest way to install markdust is to use `pip`:

``` sourceCode
pip install markdust
```

Or you can clone the [github repo](https://github.com/thespacedoctor/markdust) and install from a local version of the code:

``` sourceCode
git clone git@github.com:thespacedoctor/markdust.git
cd markdust
python setup.py install
```

To upgrade to the latest version of markdust use the command:

``` sourceCode
pip install markdust --upgrade
```

Documentation
=============

Documentation for markdust is hosted by [Read the Docs](http://markdust.readthedocs.org/en/stable/) (last [stable version](http://markdust.readthedocs.org/en/stable/) and [latest version](http://markdust.readthedocs.org/en/latest/)).

Command-Line Tutorial
=====================

Once *markdust* has been install on your machine you will have access to it’s command-line tools. This first set of commands are for working with bible passages.

Bible Passage Audio
-------------------

To generate the URL to an mp3 of a narrated bible passage, run the command:

``` sourceCode
esv audio matt 7:7-11
```

This spits out the following URL:

``` sourceCode
http://audio.esvbible.org/hw/40007007-40007011.mp3 
```

Better still, use the -i flag to generate a little iframe element that will allow you to play the audio straight from a webpage:

``` sourceCode
esv -i audio matt 7:7-11
```

Here’s the output:

``` sourceCode
<iframe width="300" height="26" frameBorder="0" allowTransparency="true" src="http://audio.esvbible.org/embed/ml/hq/40007007-40007011.mp3?scrubberWidth=100&bgcolor=615d61"></iframe>
```

which looks like this when rendered:

<iframe width="300" height="26" frameBorder="0" allowTransparency="true" src="http://audio.esvbible.org/embed/ml/hq/40007007-40007011.mp3?scrubberWidth=100&bgcolor=615d61"></iframe>
Bible Passage Text
------------------

To grab the text of a given bible passage in a markdown blockquote, run the command:

``` sourceCode
esv md matt 7:1-14
```

This command pings the [ESV API](http://www.esvapi.org/api/) and outputs the contents of the passage to the stdout along with a MD link back the passage online:

``` sourceCode
> "Judge not, that you be not judged. For with the judgment you pronounce you will be judged, and with the measure you use it will be measured to you. Why do you see the speck that is in your brother's eye, but do not notice the log that is in your own eye? Or how can you say to your brother, 'Let me take the speck out of your eye,' when there is the log in your own eye? You hypocrite, first take the log out of your own eye, and then you will see clearly to take the speck out of your brother's eye.

> "Do not give dogs what is holy, and do not throw your pearls before pigs, lest they trample them underfoot and turn to attack you.

> "Ask, and it will be given to you; seek, and you will find; knock, and it will be opened to you. For everyone who asks receives, and the one who seeks finds, and to the one who knocks it will be opened. Or which one of you, if his son asks him for bread, will give him a stone? Or if he asks for a fish, will give him a serpent? If you then, who are evil, know how to give good gifts to your children, how much more will your Father who is in heaven give good things to those who ask him!

> "So whatever you wish that others would do to you, do also to them, for this is the Law and the Prophets.

> "Enter by the narrow gate. For the gate is wide and the way is easy that leads to destruction, and those who enter by it are many. For the gate is narrow and the way is hard that leads to life, and those who find it are few."

>  **[Matthew 7:1-14](http://www.esvbible.org/matt7:1-14)** [(ESV)](http://www.esvbible.org/matt7:1-14) 
```

To also include an iframe with the audio narration of the same passage, again use the -i flag:

``` sourceCode
esv -i md matt 7:1-14
```
