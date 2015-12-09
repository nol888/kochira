"""
Automatic corrections for keywords.

This service enables the bot to perform automatic corrections for given
keywords.
"""

import re2
from peewee import CharField
from tornado.web import RequestHandler, Application

from kochira.db import Model

from kochira.service import Service
from kochira.auth import requires_permission

service = Service(__name__, __doc__)


@service.model
class Correction(Model):
    what = CharField(255)
    correction = CharField(255)

    class Meta:
        indexes = (
            (("what",), True),
        )


def is_regex(what):
    return what[0] == "/" and what[-1] == "/"


@service.command(r"stop correcting (?P<what>.+)$", mention=True)
@service.command(r"don't correct (?P<what>.+)$", mention=True)
@service.command(r"remove correction for (?P<what>.+)$", mention=True)
@requires_permission("autocorrect")
def remove_correction(ctx, what):
    """
    Remove correction.

    Remove the correction for `what`.
    """

    if not Correction.select().where(Correction.what == what).exists():
        ctx.respond(ctx._("I'm not correcting \"{what}\".").format(
            what=what
        ))
        return

    Correction.delete().where(Correction.what == what).execute()

    ctx.respond(ctx._("Okay, I won't correct {what} anymore.").format(
        what=what if is_regex(what) else "\"" + what + "\""
    ))


def match_case(original, target):
    if original.isupper():
        return target.upper()

    if original.islower():
        return target.lower()

    if original.title() == original:
        return target.title()

    if original.capitalize() == original:
        return target.capitalize()

    return target


def make_word_regex(w):
    buf = []

    for c in w:
        c_lower = c.lower()
        c_upper = c.upper()
        if c_lower != c_upper:
            # We have to be careful, because "ß".upper() == "SS".
            buf.append(r'(?:{}|{})'.format(re.escape(c_lower), re.escape(c_upper)))
        else:
            buf.append(re.escape(c))

    return r'\b{}\b'.format(''.join(buf))


@service.hook("channel_message")
def do_correction(ctx, target, origin, message):
    corrections = list(Correction.select())

    all_exprs = '|'.join('({})'.format(correction.what[1:-1]
                                       if is_regex(correction.what)
                                       else make_word_regex(correction.what))
                         for correction in corrections)

    def corrector(match):
        for i, correction in enumerate(corrections):
            match_text = match.group(i)
            if match_text is not None:
                return "\x1f" + match_case(match_text, correction.correction) + "\x1f"

    corrected = re2.sub(all_exprs, corrector, message)

    if message != corrected:
        ctx.message(ctx._("<{origin}> {corrected}").format(
            origin=origin,
            corrected=corrected
        ))


@service.command(r"correct (?P<what>.+?) to (?P<correction>.+)$", mention=True)
@requires_permission("autocorrect")
def add_correction(ctx, what, correction):
    """
    Add correction.

    Add an automatic correction for whenever someone says `what`. `what` can be a
    regular expression delimited by ``/``, e.g. ``/^foo$/``.
    """

    if Correction.select().where(Correction.what == what).exists():
        ctx.respond(ctx._("I'm already correcting {what}.").format(
            what=what if is_regex(what) else "\"" + what + "\""
        ))
        return

   if is_regex(what):
       try:
           re2.compile(what[1:-1])
        except re2.RegexError as e:
            ctx.respond(ctx._("Sorry, that's not a valid regex: {message}").format(
                e.args[0].decode('utf-8')))

    Correction.create(what=what, correction=correction).save()

    ctx.respond(ctx._("Okay, I'll correct {what}.").format(
        what=what if is_regex(what) else "\"" + what + "\""
    ))


@service.command(r"what do you correct\??$", mention=True)
@service.command(r"corrections\??$", mention=True)
def list_corrections(ctx):
    """
    List corrections.

    List all corrections the bot has registered.
    """

    ctx.respond(ctx._("I correct the following: {corrections}").format(
        corrections=", ".join(correction.what if is_regex(correction.what) else "\"" + correction.what + "\""
                              for correction in Correction.select().order_by(Correction.what))
    ))


class IndexHandler(RequestHandler):
    def get(self):
        self.render("autocorrect/index.html",
                    corrections=Correction.select().order_by(Correction.what),
                    is_regex=is_regex)


def make_application(settings):
    return Application([
        (r"/", IndexHandler)
    ], **settings)


@service.hook("services.net.webserver")
def webserver_config(ctx):
    return {
        "name": "autocorrect",
        "title": "Autocorrect",
        "application_factory": make_application
    }
