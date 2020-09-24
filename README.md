**Note: This repo is unmaintained and has been for a while. If you are
interested in taking over this repo, then please let me know (trentm at
google's email thing).**

* * *

A small Django app that provides template tags for using
[Markdown](http://daringfireball.net/projects/markdown/) using the
[python-markdown2](https://github.com/trentm/python-markdown2) library.

# What's with the "deux" in the name?

The obvious name for this project is `django-markdown2`. However, there
[already is one!](http://github.com/svetlyak40wt/django-markdown2) and name
confusion doesn't help anybody. Plus, I took French immersion in school for 12
years: might as well put it to use.

# So why another project then?

Because I wanted to do something slightly different. Django-markdown2's
`markdown` filter takes
["extras"](https://github.com/trentm/python-markdown2/wiki/Extras) as arguments
-- with the one exception that "safe" is transformed to python-markdown2's
`safe_mode` argument. This is handy for quick usage. My use case is more
commonly: lots of `markdown` filter and block usage in my Django templates with
the same set of python-markdown2 options.


# Installation

Choose the *one* of the following that works best for you:

- Install the latest release from PyPI:

        pip install django-markdown-deux

    or, if you use [ActivePython](http://www.activestate.com/activepython):

        pypm install django-markdown-deux

    These should install the dependent `python-markdown2` package.

- Get a git clone of the source tree:

        git clone git://github.com/trentm/django-markdown-deux.git

    You might want a particular tag:

        cd django-markdown-deux
        git tag -l   # list available tags
        git checkout $tagname

    Then you'll need the "lib" subdir on your PYTHONPATH:

        python setup.py install # or 'export PYTHONPATH=`pwd`/lib:$PYTHONPATH'

    You'll also need the [python-markdown2
    library](https://github.com/trentm/python-markdown2):

        git clone git@github.com:trentm/python-markdown2.git
        cd python-markdown2
        python setup.py install   # or 'export PYTHONPATH=`pwd`/python-markdown2/lib'


# Django project setup

1. Add `markdown_deux` to `INSTALLED_APPS` in your project's "settings.py".

2. Optionally set some of the `MARKDOWN_DEUX_*` settings. See the "Settings"
   section below.


# Usage

The `markdown_deux` facilities typically take an optional "style" argument. This
is a name for a set of options to the `python-markdown2` processor. There is
a "default" style that is used if no argument is given. See the
`MARKDOWN_DEUX_STYLES` setting below for more.

## `markdown` template filter

    {% load markdown_deux_tags %}
    ...
    {{ myvar|markdown:"STYLE" }}      {# convert `myvar` to HTML using the "STYLE" style #}
    {{ myvar|markdown }}              {# same as `{{ myvar|markdown:"default"}}` #}

## `markdown` template block tag

    {% load markdown_deux_tags %}
    ...
    {% markdown STYLE %}        {# can omit "STYLE" to use the "default" style #}
    This is some **cool**
    [Markdown](http://daringfireball.net/projects/markdown/)
    text here.
    {% endmarkdown %}

## `markdown_allowed` template tag

In a template:

    {% markdown_allowed %}

will emit a short HTML blurb that says Markdown syntax is allowed. This can be
handy for placing under form elements that accept markdown syntax. You can also
use it as the `help_text` for a form field something like:

    # myapp/forms.py
    from markdown_deux.templatetags.markdown_deux_tags import markdown_allowed
    class MyForm(forms.Form):
        #...
        description = forms.CharField(
            label="Description (required)",
            widget=forms.Textarea(attrs={"rows": 5}),
            help_text=_secondary_span("A brief description of your thing.<br/> "
                + markdown_allowed()),
            required=True)


## `markdown_cheatsheet` tag

    {% markdown_cheatsheet %}

This outputs HTML giving a narrow (appropriate for, e.g., a sidebar) listing of
some of the more common Markdown features.


## `markdown_deux.markdown(TEXT, STYLE)` in your Python code

The `markdown` filter and block tags above ultimately use this
`markdown_deux.markdown(...)` function. You might find it useful to do Markdown
processing in your Python code (e.g. in a view, in a model `.save()` method).


# Settings

All settings for this app are optional.

## `MARKDOWN_DEUX_STYLES` setting

A mapping of style name to a dict of keyword arguments for python-markdown2's
`markdown2.markdown(text, **kwargs)`. For example the default setting is
effectively:

    MARKDOWN_DEUX_STYLES = {
        "default": {
            "extras": {
                "code-friendly": None,
            },
            "safe_mode": "escape",
        },
    }

I.e. only the "default" style is defined and it just uses the [code-friendly
extra](https://github.com/trentm/python-markdown2/wiki/code-friendly) and escapes
raw HTML in the given Markdown (for safety).

Here is how you might add styles of your own, and preserve the default style:

    # settings.py
    from markdown_deux.conf.settings import MARKDOWN_DEUX_DEFAULT_STYLE

    MARKDOWN_DEUX_STYLES = {
        "default": MARKDOWN_DEUX_DEFAULT_STYLE,
        "trusted": {
            "extras": {
                "code-friendly": None,
            },
            # Allow raw HTML (WARNING: don't use this for user-generated
            # Markdown for your site!).
            "safe_mode": False,
        }
        # Here is what http://code.activestate.com/recipes/ currently uses.
        "recipe": {
            "extras": {
                "code-friendly": None,
            },
            "safe_mode": "escape",
            "link_patterns": [
                # Transform "Recipe 123" in a link.
                (re.compile(r"recipe\s+#?(\d+)\b", re.I),
                 r"http://code.activestate.com/recipes/\1/"),
            ],
            "extras": {
                "code-friendly": None,
                "pyshell": None,
                "demote-headers": 3,
                "link-patterns": None,
                # `class` attribute put on `pre` tags to enable using
                # <http://code.google.com/p/google-code-prettify/> for syntax
                # highlighting.
                "html-classes": {"pre": "prettyprint"},
                "cuddled-lists": None,
                "footnotes": None,
                "header-ids": None,
            },
            "safe_mode": "escape",
        }
    }


## `MARKDOWN_DEUX_HELP_URL` setting

A URL for to which to link for full markdown syntax default. This link is
only in the output of the `markdown_allowed` and `markdown_cheatsheet`
template tags.

The default is <http://daringfireball.net/projects/markdown/syntax>, the
canonical Markdown syntax reference. However, if your site uses Markdown with
specific tweaks, you may prefer to have your own override. For example,
[ActiveState Code](http://code.activestate.com) uses:

    MARKDOWN_DEUX_HELP_URL = "/help/markdown/"

To link to [its own Markdown syntax notes
URL](http://code.activestate.com/help/markdown/).
