#!/usr/bin/env python
# Copyright (c) 2008-2010 ActiveState Corp.
# License: MIT (http://www.opensource.org/licenses/mit-license.php)

r"""A small Django app that provides template tags for Markdown using the
python-markdown2 library.

See <http://github.com/trentm/django-markdown-deux> for more info.
"""

__version_info__ = (1, 0, 5)
__version__ = '.'.join(map(str, __version_info__))
__author__ = "Trent Mick"


def markdown(text, style="default"):
    if not text:
        return ""
    import markdown2
    return markdown2.markdown(text, **get_style(style))

def get_style(style):
    from markdown_deux.conf import settings
    try:
        return settings.MARKDOWN_DEUX_STYLES[style]
    except KeyError:
        return settings.MARKDOWN_DEUX_STYLES.get("default",
            settings.MARKDOWN_DEUX_DEFAULT_STYLE)
