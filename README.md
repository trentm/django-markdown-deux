A small Django app that provides template tags for using
[Markdown](http://daringfireball.net/projects/markdown/) using the
[python-markdown2](http://code.google.com/p/python-markdown2/) library.

# What with the "deux" in the name?

The obvious name for this project in `django-markdown2`. However, there
[already is one!](http://github.com/svetlyak40wt/django-markdown2) and name
confusion doesn't help anybody.

# So why another project then?

Because I wanted to do something slightly different. Django-markdown2's
`markdown` filter takes
["extras"](http://code.google.com/p/python-markdown2/wiki/Extras) as arguments
-- with the one exception that "safe" is transformed to python-markdown2's
"safe_mode" argument. This is handy for quick usage. My use case is more
commonly: lots of `markdown` filter and block usage in my Django templates with
the same set of python-markdown2 options.


# Installation

TODO

# Django project setup

TODO

# Usage

TODO

