# Copyright (c) 2010 ActiveState Software Inc.

from django.conf import settings

MARKDOWN_DEUX_HELP_URL = getattr(settings, "MARKDOWN_DEUX_HELP_URL",
    "http://daringfireball.net/projects/markdown/syntax")

MARKDOWN_DEUX_DEFAULT_STYLE = {
    "extras": {
        "code-friendly": None,
    },
    "safe_mode": "escape",
}

MARKDOWN_DEUX_STYLES = getattr(settings, "MARKDOWN_DEUX_STYLES",
    {"default": MARKDOWN_DEUX_DEFAULT_STYLE})

DEBUG = settings.DEBUG
