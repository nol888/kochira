"""
Sed-style find and replacement.

Finds patterns in text and replaces it with other terms.
"""

import re

from kochira.service import Service

service = Service(__name__, __doc__)


@service.command(r"s(.)(?P<pattern>(?:[^\1]|\\1)+)\1(?P<replacement>(?:[^\1]|\\1)+)\1(?P<flags>[is]*)", eat=False)
@service.command(r"(?P<who>.+?)[,;:]? s(.)(?P<pattern>(?:[^\2]|\\2)+)\2(?P<replacement>(?:[^\1]|\\2)+)\2(?P<flags>[is]*)", eat=False)
def sed(ctx, pattern, replacement, who=None, flags=None):
    """
    Find and replace.

    Find a regular expression pattern and replace it. Regular expressions are implicitly global.
    Flags supported are `i` for case insensitive, and `s` for dot-all.
    """

    if flags is None:
        flags = ""

    re_flags = re.UNICODE

    if "i" in flags:
        re_flags |= re.IGNORECASE
    if "s" in flags:
        re_flags |= re.DOTALL

    try:
        expr = re.compile(pattern, re_flags)
    except:
        ctx.respond(ctx._("Couldn't parse that pattern."))
        return

    for other, message in list(ctx.client.backlogs.get(ctx.target, []))[1:]:
        if who is None or other == who:
            match = expr.search(message)

            if match is not None:
                try:
                    msg = expr.sub("\x1f" + replacement + "\x1f", message)
                except:
                    ctx.respond(ctx._("Couldn't parse that pattern."))
                    return

                ctx.message("<{who}> {message}".format(who=other, message=msg))
                break
